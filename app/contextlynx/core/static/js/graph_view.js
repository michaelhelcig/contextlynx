window.renderKnowledgeGraph = function(data) {
    // Function to set SVG size based on window size
    function updateSize() {
        width = window.innerWidth;
        height = window.innerHeight;
        svg.attr("width", width).attr("height", height);
        simulation.force("center", d3.forceCenter(width / 2, height / 2));
        backgroundRect.attr("width", width).attr("height", height);
    }

    // Set initial SVG size
    let width = window.innerWidth;
    let height = window.innerHeight;

    const container = d3.select("#knowledge-graph")
        .style("width", "100%")
        .style("height", "100vh")
        .style("overflow", "hidden");

    const svg = container.append("svg")
        .attr("width", width)
        .attr("height", height);

    // Create a pattern for the background
    const defs = svg.append("defs");
    const pattern = defs.append("pattern")
        .attr("id", "dot-pattern")
        .attr("width", 10)
        .attr("height", 10)
        .attr("patternUnits", "userSpaceOnUse");

    pattern.append("circle")
        .attr("cx", 5)
        .attr("cy", 5)
        .attr("r", 1)
        .attr("fill", "#ccc");

    // Create a group for the graph elements
    const g = svg.append("g");

    const simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(d => d.id).distance(d => 400 * (1 - d.similarity)))
        .force("charge", d3.forceManyBody().strength(-800))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius(d => d.radius + 15));

    const gradientToColor = (targetColor) => {
        return d3.scaleLinear()
            .domain([0, 1])
            .range(["white", targetColor]);
    };

    const link = g.append("g")
        .selectAll("line")
        .data(data.links)
        .join("line")
        .attr("stroke", d => gradientToColor(d.color)(d.similarity))
        .attr("stroke-opacity", 0.8)
        .attr("stroke-width", 2);

    const node = g.append("g")
        .selectAll("g")
        .data(data.nodes)
        .join("g")
        // Attach drag functionality
        .call(drag(simulation));

    // Add event listener for click on NodeNote type
    node.on("click", (event, d) => {
        if (d.type === "NodeNote") {
            const url = `/notes/${d.uuid}/related`;
            window.location.href = url;
        }
    });

    function calculateRadius(d) {
        const baseRadius = d.type === "NodeTopic" ? 40 + 2 * d.edgeCount : 30;
        const titleLength = d.title.length;
        return Math.max(baseRadius, Math.sqrt(titleLength * 30));
    }

    function calculateFontSize(d) {
        return d.type === "NodeTopic" ? "10px" : "8px";
    }

    const circles = node.append("circle")
        .attr("r", d => {
            d.radius = calculateRadius(d);
            return d.radius;
        })
        .attr("fill", d => d.color);

    function fitTextInCircle(text, radius, fontSize) {
        const words = text.split(/\s+/);
        let lines = [];
        let line = [];
        let totalHeight = 0;
        const lineHeight = parseInt(fontSize, 10) * 1.2;
        const maxWidth = radius * 1.8;

        for (let word of words) {
            line.push(word);
            const testLine = line.join(" ");
            const testWidth = getTextWidth(testLine, `${fontSize} Arial`);

            if (testWidth > maxWidth) {
                if (line.length === 1) {
                    lines.push(line[0]);
                    totalHeight += lineHeight;
                } else {
                    line.pop();
                    lines.push(line.join(" "));
                    totalHeight += lineHeight;
                    line = [word];
                }
            }
        }

        if (line.length > 0) {
            lines.push(line.join(" "));
            totalHeight += lineHeight;
        }

        while (totalHeight > radius * 1.8 && lines.length > 1) {
            lines.pop();
            totalHeight -= lineHeight;
        }

        if (totalHeight > radius * 1.8) {
            let lastLine = lines[lines.length - 1];
            while (getTextWidth(lastLine + "...", `${fontSize} Arial`) > maxWidth) {
                lastLine = lastLine.slice(0, -1);
            }
            lines[lines.length - 1] = lastLine + "...";
        }

        return lines;
    }

    function getTextWidth(text, font) {
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        context.font = font;
        return context.measureText(text).width;
    }

    const texts = node.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", ".35em")
        .style("fill", "black")
        .style("font-size", d => calculateFontSize(d))
        .each(function(d) {
            const fontSize = calculateFontSize(d);
            const lines = fitTextInCircle(d.title, d.radius, fontSize);
            const text = d3.select(this);
            lines.forEach((line, i) => {
                text.append("tspan")
                    .attr("x", 0)
                    .attr("dy", (i === 0 ? -(lines.length - 1) * 0.5 : 1) + "em")
                    .text(line);
            });
        });

    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("transform", d => `translate(${d.x},${d.y})`);
    });

    function drag(simulation) {
        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    // Add zoom behavior
    const zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on("zoom", (event) => {
            g.attr("transform", event.transform);
        });

    svg.call(zoom);

    // Update size on window resize
    window.addEventListener('resize', updateSize);

    console.log("Knowledge graph rendered with", data.nodes.length, "nodes and", data.links.length, "links");
};

// Initial render
window.renderKnowledgeGraph(data);