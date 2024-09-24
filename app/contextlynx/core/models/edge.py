from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from .project import Project
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .node import Node
from django.db import connection
import uuid

class Edge(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    predicted = models.BooleanField(default=False)

    from_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='from_edges')
    from_object_id = models.PositiveIntegerField()
    from_node = GenericForeignKey('from_content_type', 'from_object_id')

    to_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='to_edges')
    to_object_id = models.PositiveIntegerField()
    to_node = GenericForeignKey('to_content_type', 'to_object_id')

    similarity = models.FloatField(null=True)

    @classmethod
    def ensure_edge(cls, node1, node2, predicted=False, similarity=None):
        # Check if an edge exists in either direction
        edge = None

        if node1.has_edge_to(node2):
            edge = node1.edge_to(node2)  # Get the edge from node1 to node2
        elif node2.has_edge_to(node1):
            edge = node2.edge_to(node1)  # Get the edge from node2 to node1

        if edge:
            # If an edge exists, update it

            # ensure the edge is not accidentally set to predicted
            if edge.predicted:
                edge.predicted = predicted

            edge.similarity = similarity
            edge.save()
        else:
            # If no edge exists, create a new one
            Edge.objects.create(
                project=node1.project,
                from_node=node1,
                to_node=node2,
                predicted=predicted,
                similarity=similarity
            )

    @staticmethod
    def get_for_nodes(nodes):
        node_ct = ContentType.objects.get_for_model(Node)

        node_ids = nodes.values_list('id', flat=True)
        node_ct_ids = [node_ct.id] * len(node_ids)  # Same content type for all nodes

        # Filter edges where the 'from_node' matches these node IDs
        froms = Edge.objects.filter(
            from_content_type=node_ct,
            from_object_id__in=node_ids
        )

        tos = Edge.objects.filter(
            to_content_type=node_ct,
            to_object_id__in=node_ids
        )

        return froms.union(tos)

    @classmethod
    def get_n_largest_nodes(cls, project, content_type, n=10):
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH ranked_nodes AS (
                    SELECT DISTINCT ON (node_id)
                        COALESCE(from_object_id, to_object_id) as node_id,
                        CASE
                            WHEN from_object_id IS NOT NULL THEN from_content_type_id
                            ELSE to_content_type_id
                        END as content_type_id,
                        COUNT(*) OVER (PARTITION BY COALESCE(from_object_id, to_object_id)) as edge_count
                    FROM 
                        %(edge_table)s
                    WHERE 
                        project_id = %%s AND
                        (
                            (from_content_type_id = %%s AND from_object_id IS NOT NULL) OR
                            (to_content_type_id = %%s AND to_object_id IS NOT NULL)
                        )
                )
                SELECT node_id, content_type_id, edge_count
                FROM ranked_nodes
                ORDER BY edge_count DESC
                FETCH FIRST %%s ROWS ONLY
            """ % {'edge_table': cls._meta.db_table},
                           [project.id, content_type.id, content_type.id, n])

            return cursor.fetchall()

    @classmethod
    def get_n_nearest_nodes(cls, node, content_type, n=10, max_depth=5):
        """
        Retrieve up to 'n' nearest nodes of a specified content type from a given node,
        ensuring all are in the same connected cluster.

        This method uses a breadth-first search on the graph, starting from the node,
        to find the closest nodes based on depth (edges traversed) and similarity.

        Parameters:
        - node: Starting node.
        - content_type: Type of nodes to return.
        - n: Max number of nodes (default: 10).
        - max_depth: Max search depth (default: 5).

        Returns:
        A list of tuples (node_id, content_type_id, similarity, depth) for the nearest nodes.
        The search ensures only connected nodes are considered, within the depth, avoiding cycles.
        """
        start_node_id = node.id
        content_type_id = content_type.id
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH RECURSIVE connected_nodes AS (
                    -- Base case: start with the given node
                    SELECT 
                        %s::integer AS start_node_id,
                        %s::integer AS start_content_type_id,
                        CASE 
                            WHEN from_object_id = %s AND from_content_type_id = %s THEN to_object_id 
                            ELSE from_object_id 
                        END AS node_id,
                        CASE 
                            WHEN from_object_id = %s AND from_content_type_id = %s THEN to_content_type_id 
                            ELSE from_content_type_id 
                        END AS content_type_id,
                        similarity,
                        1 AS depth,
                        ARRAY[CASE 
                            WHEN from_object_id = %s AND from_content_type_id = %s THEN to_object_id 
                            ELSE from_object_id 
                        END] AS visited_nodes
                    FROM 
                        """ + cls._meta.db_table + """
                    WHERE 
                        (from_object_id = %s AND from_content_type_id = %s) OR 
                        (to_object_id = %s AND to_content_type_id = %s)
                
                    UNION ALL
                
                    -- Recursive case: find connected nodes
                    SELECT 
                        cn.start_node_id,
                        cn.start_content_type_id,
                        CASE 
                            WHEN e.from_object_id = cn.node_id AND e.from_content_type_id = cn.content_type_id 
                            THEN e.to_object_id 
                            ELSE e.from_object_id 
                        END AS node_id,
                        CASE 
                            WHEN e.from_object_id = cn.node_id AND e.from_content_type_id = cn.content_type_id 
                            THEN e.to_content_type_id 
                            ELSE e.from_content_type_id 
                        END AS content_type_id,
                        e.similarity,
                        cn.depth + 1 AS depth,
                        cn.visited_nodes || CASE 
                            WHEN e.from_object_id = cn.node_id AND e.from_content_type_id = cn.content_type_id 
                            THEN e.to_object_id 
                            ELSE e.from_object_id 
                        END AS visited_nodes
                    FROM 
                        """ + cls._meta.db_table + """ e
                    INNER JOIN 
                        connected_nodes cn ON 
                        ((e.from_object_id = cn.node_id AND e.from_content_type_id = cn.content_type_id) OR 
                         (e.to_object_id = cn.node_id AND e.to_content_type_id = cn.content_type_id))
                    WHERE 
                        cn.depth < %s
                        AND NOT (CASE 
                            WHEN e.from_object_id = cn.node_id AND e.from_content_type_id = cn.content_type_id 
                            THEN e.to_object_id 
                            ELSE e.from_object_id 
                        END) = ANY(cn.visited_nodes)
                )
                SELECT DISTINCT ON (node_id, content_type_id)
                    node_id, 
                    content_type_id, 
                    similarity, 
                    depth
                FROM 
                    connected_nodes
                WHERE 
                    (node_id != start_node_id OR content_type_id != start_content_type_id)
                    AND content_type_id = %s
                ORDER BY 
                    node_id, content_type_id, depth ASC, similarity DESC
                LIMIT %s
            """, [start_node_id, content_type_id, start_node_id, content_type_id, start_node_id, content_type_id,
                  start_node_id, content_type_id, start_node_id, content_type_id, start_node_id, content_type_id,
                  max_depth, content_type_id, n])

            return cursor.fetchall()

    def __str__(self):
        return f"{self.from_node} -> {self.to_node} ({self.similarity})"
