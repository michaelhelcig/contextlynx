import google.generativeai as genai
import json

# Replace with your actual API key
API_KEY = 'AIzaSyCadQ9jJqUbtWqmH-3x1h_Efml8uQedQeQ'

# Configure the API key
genai.configure(api_key=API_KEY)

# Define the existing topics
existing_topics = [
        "Electric Vehicles",
        "Renewable Energy",
        "Automotive Industry",
        "Energy Storage Solutions",
        "Solar Energy",
        "Geography",
        "Business History",
        "Innovation in Technology",
        "Entrepreneurship and Leadership",
        "Elon Musk",
        "Clean Energy Solutions"
    ]

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_topics(text):
    # Convert existing topics to a string format suitable for the prompt
    existing_topics_str = ', '.join(existing_topics)
    
    # Design the prompt to get topics, filter out specific entities, and compare with existing topics
    prompt = f"""
    Analyze the following text to extract the main topics. 

    - Include specific names of companies, people, cities, and other named entities as potential topics.
    - Include the overall themes or subjects discussed in the text as topics.
    - Summarize the main topic in the text.
    - Filter out irrelevant information and focus on these named entities along with general topics.
    - Compare the extracted topics with the list of existing topics provided.
    - For each topic, determine if it is new (i.e., not in the list of existing topics) or if it matches one of the existing topics.
    - Return the Topics in Title Case

    Return the results as a JSON array where each entry is an object with two fields:
    - "topic": the name of the topic
    - "is_new": a boolean indicating whether the topic is new (True) or not (False)

    Use this JSON schema. Don't format as markdown with ```.:
    topic = {{'topic': str, 'is_new': boolean}}
    Return: list[topic]
    
    
    ----------
    Existing topics: [{existing_topics_str}]
    Text: 
    {text}

    """
    
    # Generate content using the model
    response = model.generate_content(prompt)
    
    # Parse the response assuming it is in JSON format
    try:
        # check if wrapped in markdown
        if response.text.startswith("```json"):
            response_text = response.text[8:-3]
        else:
            response_text = response.text
        results = json.loads(response_text)
    except json.JSONDecodeError:
        print("Failed to parse JSON response:")
        print(response.text)
        results = []
    
    return results

def generate_summary(text):
    # Design the prompt to generate a summary of the text
    prompt = f"""
    Generate a concise summary of the following text:
    Describe the main points and key information in a few sentences. Also why this text is important.
    Make sure that all important aspects are covered in the summary.
    The summary should refelct the length and complexity of the original text.

    {text}
    """
    
    # Generate content using the model
    response = model.generate_content(prompt)
    
    return response.text


def main():
    # Example text input
    text = "Tesla, Inc., founded by Martin Eberhard and Marc Tarpenning in 2003, is a pioneering electric vehicle and clean energy company led by Elon Musk. The company is renowned for its innovative electric cars, such as the Model S, Model 3, Model X, and Model Y, which have significantly advanced the electric vehicle market. Tesla's advancements extend beyond cars; it also focuses on renewable energy solutions, including solar panels and energy storage products like the Powerwall. With a mission to accelerate the world's transition to sustainable energy, Tesla has become a major force in reshaping the automotive and energy industries."

    text = """
# Donald Trump Interview | Lex Fridman Podcast #442
# https://www.youtube.com/watch/qCbfTN-caFI

00:00:00.000 I don't know if you know this,
00:00:00.833 but some people call you a fascist.
00:00:03.270 Yeah, they do.
00:00:04.290 So I figure it's all rightto call them a communist.
00:00:06.600 Yeah, they call me a lotworse than I call them.
00:00:08.820 A lot of people listeningto this, myself included,
00:00:12.120 that doesn't think thatKamala is a communist.
00:00:15.600 I believe you have tofight fire with fire.
00:00:17.940 Politics is a dirty game.
00:00:19.390 It is a dirty game. It's certainly true.
00:00:21.990 How do you win at that game?
00:00:23.970 They suffer from
00:00:24.870 massive Trump derangement syndrome, TDS,
00:00:31.680 and I don't know if it'scurable from their standpoint.
00:00:35.340 I think we would probablyhave a better world
00:00:38.220 if everybody in Congresstook some mushrooms, perhaps.
00:00:41.190 First of all, medicalmarijuana has been amazing.
00:00:46.200 I've had friends and I've had others
00:00:48.420 and doctors telling me thatit's been absolutely amazing.
00:00:53.040 The list of clients that went
00:00:54.960 to the island has not been made public.
00:00:57.720 Yeah, it's very interesting, isn't it?
00:01:03.330 The following is a conversationwith Donald Trump on this,
00:01:06.900 the Lex Fridman podcast.
00:01:09.540 They getting smaller and smaller.
00:01:11.122 They getting smaller.
00:01:12.330 I mean, people do respect you more
00:01:14.520 when you have a bigcamera for some reason.
00:01:15.353 No, it's cool.
00:01:16.380 And about 20 guys that youpay a fortune to, right?
00:01:18.810 Alright. Okay, you saidthat you love winning
00:01:24.630 and you have won a lot in life,in real estate, in business,
00:01:29.100 in TV and politics.
00:01:30.900 So let me start with amindset, a psychology question.
00:01:36.510 What drives you more?
00:01:37.920 The love of winning or the hate of losing?
00:01:41.160 Maybe equally, maybe both.
00:01:44.580 I don't like losing and I do like winning.
00:01:47.790 I've never thought of it as to
00:01:49.470 which is more of a driving force.
00:01:51.960 You've been close with alot of the greats in sport.
00:01:55.830 You think about Tiger Woods, Muhammad Ali,
00:01:58.980 you have people like Michael Jordan
00:02:00.840 who I think hate losing more than anybody.
00:02:04.470 So what do you learn from those guys?
00:02:06.750 Well, they do have something different.
00:02:08.340 You know, the great championshave something very different
00:02:11.610 like the sports champions
00:02:13.140 and you know, you havechampions in other fields,
00:02:16.080 but you see it more readily in sports.
00:02:18.000 You see it over a weekendor you see it during a game
00:02:21.060 and you see that certain people stand out
00:02:23.670 and they keep standing out.
00:02:27.540 But it's there for you.
00:02:28.500 It doesn't take a lifetime
00:02:29.970 to find out that somebodywas a winner or a loser.
00:02:33.660 And so the sports thingis very interesting.
00:02:35.940 But you know, I play golfwith different people
00:02:39.390 and there's a differentmindset among champions.
00:02:44.850 There's really a very different mindset.
00:02:48.269 There's a different thought process.
00:02:50.130 You know, talent wise,
00:02:51.840 sometimes you can't tellthe difference in talent,
00:02:53.910 but at the end of aweekend they seem to win.
00:02:58.020 And it's very interesting,like as an example,
00:03:01.800 Tiger or Jack Nicholas,he was a phenomenal winner
00:03:06.060 and he does have adifferent way about him.
00:03:08.040 And Tiger has a different wayabout him and Michael Jordan.
00:03:11.640 And you would thinkthat there'd be one way.
00:03:15.000 Arnold Palmer was thenicest guy you'd ever meet.
00:03:18.600 And then you have some championsthat aren't really nice.
00:03:21.840 They're just focused on doing their job.
00:03:25.500 So you have, you know, there'snot one type of person.
00:03:29.850 But the one thing I wouldsay that everybody seems
00:03:33.960 to have in common is they're very driven.
00:03:37.050 They're driven like beyond.
00:03:39.810 They don't seem to give up easily.
00:03:41.340 They don't give up. They don't give up.
00:03:43.830 But they do seem to be, youknow, they have a passion
00:03:46.800 that's maybe more thanpeople that don't do as well.
00:03:51.480 You've said thatpolitics is a dirty game
00:03:54.540 in the past
00:03:55.540 It is a dirty game.
00:03:56.910 It's certainly true.
00:03:59.130 So if it is a game, howdo you win at that game?
00:04:02.310 Well, you win at thatgame by getting the word out
00:04:05.490 and by using sense.
00:04:08.670 You have to have afeeling where it's going.
00:04:11.730 You also have to have afeeling of what's right.
00:04:13.560 You can't necessarilyjust go, what's popular?
00:04:15.690 You have to do what's good for a country,
00:04:17.190 if you're talking about countries.
00:04:19.140 But you have to get the word out
00:04:20.880 and you have to justcontinuously, like for instance,
00:04:23.340 you have a great show,you have a great podcast,
00:04:25.800 it's very well watched.
00:04:27.630 And I'm sitting here and I dothis, a lot of people see it
00:04:30.480 and I do other things anda lot of people see that.
00:04:34.230 And I go traditional also, you know,
00:04:35.817 you have traditional television,
00:04:37.800 which is getting a little bit older
00:04:40.800 and maybe less significant,
00:04:42.570 could be less significant, I don't know.
00:04:45.000 But it's changing a lot.
00:04:48.480 The whole plane ofplatform is changing a lot.
00:04:52.770 It's changed a lot in thelast two, three years.
00:04:56.130 But from a politicalstandpoint, you have to find out
00:04:58.950 what people are doing,what they're watching.
00:05:01.050 And you have to get on.
00:05:03.270 I just see that these platformsare starting to dominate,
00:05:08.160 that getting very big numbers.
00:05:10.500 I did Spaces with Elon
00:05:14.250 and they got numbers likenobody's ever heard before.
00:05:16.740 So you know, you wouldn'tdo that on like radio.
00:05:23.190 No matter how good a show,
00:05:24.060 you wouldn't do those numbers on radio.
00:05:25.500 You wouldn't do them on television.
00:05:28.350 You've been successful in business,
00:05:29.970 you've been successful in politics.
00:05:31.440 What do you think is thedifference between gaining success
00:05:34.320 between the two differentdisparate worlds?
00:05:37.260 Yeah, and they'redifferent. Very different.
00:05:40.410 I have a lot of peoplethat are in business
00:05:42.210 that are successful and they'dlike to go over to politics
00:05:46.710 and then you realize theycan't speak, they choke.
00:05:52.980 You know, it's hard to make aspeech in front of thousands.
00:05:54.960 Let's say you're talkingabout a big audience,
00:05:56.910 but I get very big audiences
00:05:59.430 and you know, for many peopleit's virtually impossible
00:06:02.610 to get up and speak for an hour and a half
00:06:05.880 and have nobody leave.
00:06:09.780 You know, it's not an easything to do and it's an ability.
00:06:13.920 But I have many people thatare very, very successful
00:06:16.771 in business, would love to do what I did.
00:06:22.530 And yet they can't pull the trigger.
00:06:25.470 And in many cases Idon't think it would work
00:06:28.050 almost for everybody it's not gonna work.
00:06:30.840 It's a very tough thing to do.
00:06:33.240 It's a big transition.
00:06:34.950 And now if you talkedabout people politics
00:06:39.480 going into business,
00:06:41.100 likewise, that wouldn't generallywork out so well either.
00:06:44.940 It's different talents,it's different skills.
00:06:46.800 I have somebody who wantsto go into politics so bad,
00:06:48.960 but he's got a little problem,he's got stage fright.
00:06:52.500 Now he's a total killer,
00:06:55.560 but if he gets up into astage in front of people,
00:06:57.840 he doesn't do well, toput it mildly actually.
00:07:01.170 I mean, he does badly.
00:07:03.090 So you have to be ableto make hard decisions
00:07:06.000 like you do in business,
00:07:06.960 but also be able to captivate an audience.
00:07:09.600 Look, if you're apolitician, you have to be able
00:07:11.550 to speak in front of large crowds.
00:07:13.080 There are a lot of peoplecan't do that. I've seen it.
00:07:16.980 They can't even think aboutdoing it. And they don't.
00:07:21.300 There are many peoplein business right now,
00:07:23.310 I could name them, but Idon't wanna embarrass anybody.
00:07:26.220 They've been talking aboutrunning for president
00:07:28.080 for 15 years
00:07:30.330 and they're very big in business,very well known actually.
00:07:34.560 But it takes guts torun, like for president,
00:07:36.900 I can tell you it takes guts to run.
00:07:39.570 It's also a very dangerous profession
00:07:41.730 if you wanna know the truth,
00:07:42.720 But dangerous in a different sense too.
00:07:46.530 But it takes a lot ofcourage to run for president.
00:07:49.620 It's not easy.
00:07:50.453 But you have, and youknow, same people as I do,
00:07:54.510 there are a lot of people
00:07:55.530 that would like to run for president
00:07:56.940 that are very, verysuccessful in business,
00:08:00.750 but they don't have the guts to do it.
00:08:02.670 And they have to give up a lot.
00:08:05.040 One of the great things about people
00:08:07.350 from the business world isthey're often great deal makers,
00:08:11.550 And you're a great deal maker
00:08:13.380 and you've talked about the war in Ukraine
00:08:16.920 and that you would be able to find a deal
00:08:19.440 that both Putin andZelenskyy would accept.
00:08:22.230 What do you think that deal looks like?
00:08:24.900 I think the deal, and Iwouldn't talk about it too much
00:08:27.720 because I think I can make a deal if I win
00:08:30.900 as President-elect, I'llhave a deal made, guaranteed.
00:08:34.860 That's a war that shouldn'thave happened. It's terrible.
00:08:37.860 Look, Biden is the worst president
00:08:39.960 in the history of our country
00:08:41.850 and she's probably worse than him.
00:08:44.490 That's something thatshould have never happened,
00:08:47.520 but it did happen.
00:08:49.140 And now it's a much tougher deal to make
00:08:51.210 than it would've been before it started.
00:08:53.670 Millions of people,
00:08:55.740 I think the number's gonna be a lot higher
00:08:57.300 when you see this allat some point iron out.
00:09:00.450 I think the death numbersare gonna be a lot higher
00:09:03.270 than people think.
00:09:04.710 When you take a look at the destruction
00:09:06.630 and the buildings coming downall over the place in Ukraine,
00:09:10.560 I think those numbers aregonna be a lot higher.
00:09:12.660 They lie about the numbers.They try and keep them low.
00:09:15.600 They knock down a buildingthat's two blocks long.
00:09:17.610 These are big buildings.
00:09:18.660 And they say one personwas mildly injured,
00:09:23.850 no, no, a lot of people were killed.
00:09:27.030 And there are people in those buildings
00:09:29.070 and they have no chance.
00:09:30.120 Once they start comingdown, there's no chance.
00:09:32.910 So that's a war thatabsolutely has to get done.
00:09:37.470 And then you have Israel
00:09:39.210 and then you have a lot of other places
00:09:40.710 that are talking war.
00:09:42.030 The world is a rough place right now.
00:09:45.660 And a lot of it's because of the fact
00:09:47.220 that America has no leadership.
00:09:50.040 And I believe that she'll beprobably worse than Biden.
00:09:53.610 I watched the interview the other night.
00:09:56.460 I mean, it was just a softball interview.
00:09:59.610 So you would like to see her
00:10:00.480 do more interviews, challenged more?
00:10:02.970 I don't know.
00:10:03.803 I can't believe thewhole thing is happening.
00:10:06.180 We had a man in there thatshould have never been in there.
00:10:09.210 They kept them in a basement.
00:10:10.440 They used Covid, they cheated,but they used Covid to cheat
00:10:13.200 and they cheated without Covid too.
00:10:15.600 But you had somebody in there.
00:10:18.000 And now we have a woman that is not,
00:10:20.880 I mean she couldn't do an interview.
00:10:22.980 This was a really soft interview.
00:10:24.750 This is an interview where
00:10:25.890 they're given a multiple choicequestions, multiple guess.
00:10:30.277 I call it multiple guess.
00:10:33.030 And I don't think she did well.
00:10:35.190 I think she did very poorly.
00:10:36.720 How do you think you'lldo in the debate coming up?
00:10:38.880 It's in a few days.
00:10:39.810 So I've done a lot ofdebating. Only as a politician.
00:10:43.200 I never debated,
00:10:44.100 my first debate was the RosieO'Donnell debate, right?
00:10:47.100 The famous Rosie O'Donnelldebate. The Answer.
00:10:51.180 But I've done well with debates,I mean, I became president.
00:10:53.820 Then the second time Igot millions more votes.
00:10:56.730 I only got the first time.
00:10:58.080 I was told if I got 63 million,
00:11:00.720 which is what I got thefirst time, you would win.
00:11:04.110 You can't not win.
00:11:06.390 And I got millions of more votes on that
00:11:08.760 and lost by a whisker.
00:11:13.770 And look what happened to theworld with all of the wars
00:11:16.740 and all of the problems.
00:11:17.910 And look what happened with inflation
00:11:20.550 'cause inflation's just eatingup our country, eating it up.
00:11:24.690 So it's too bad.
00:11:25.560 But there are a lot ofthings that could happen.
00:11:30.120 We have to get those wars settled.
00:11:32.640 I'll tell you, you haveto get Ukraine done.
00:11:34.650 That could end up in a third world war.
00:11:36.240 So could the Middle East.So could the Middle East.
00:11:39.450 So maybe let's talk aboutwhat it takes to negotiate
00:11:42.840 with somebody like Putin or Zelenskyy.
00:11:45.870 Do you think Putin wouldbe willing to give up
00:11:47.580 any of the regions that already captured?
00:11:49.380 I don't know.
00:11:51.150 I can tell you that all ofthis would've never happened.
00:11:55.230 And it would've been very easy
00:11:57.150 because you don't have,
00:11:58.140 like that question wouldn't be asked.
00:11:59.670 You know, that's a tougher question
00:12:01.320 once that starts happening.
00:12:03.570 'Cause he has taken overa lot of territory now.
00:12:05.550 I guess they're insurgents now too, right?
00:12:08.790 So, you know, it's alittle bit interesting
00:12:12.120 that that's happeningand that it can happen.
00:12:16.110 And it's interesting that Putinhas allowed that to happen.
00:12:21.150 Look, that's one thatshould have never started.
00:12:24.660 We have to get it stopped.Ukraine is being demolished.
00:12:29.310 They're destroying a great culture
00:12:31.050 that's largely destroyed.
00:12:32.520 What do you think works better
00:12:33.570 in those kinds of negotiations?
00:12:35.670 Leverage of, let's say friendship,
00:12:38.730 the carrot or the stick?
00:12:39.900 Friendship or sort of the threat
00:12:43.320 of using the economic and military power.
00:12:46.080 So it depends on who the person is.
00:12:48.810 Everyone's different,negotiations interesting
00:12:52.110 because it depends on who the person is.
00:12:54.780 And then you have to guess
00:12:56.430 or know through certainknowledge, which is, you know,
00:13:00.060 more important, the carrot or the stick.
00:13:03.600 And with some people it's the stick.
00:13:04.887 And with some people it's the carrot.
00:13:07.410 I think the stick probably is
00:13:10.350 generally more successfulin that, you know,
00:13:12.930 we're talking about war.
00:13:14.940 But the kind of destructionthat we're witnessing now,
00:13:19.860 nobody's ever seen, I meanit's a terrible thing.
00:13:23.010 And we're witnessing it all over.
00:13:24.960 We're witnessing it inall parts of the world.
00:13:29.580 And a lot of things aregoing to get started.
00:13:31.560 Look what's going on withChina, look at Japan.
00:13:34.830 They're starting to re-armnow they're starting to re-arm
00:13:37.380 because China's getting, you know,
00:13:39.060 taking over certain islands.
00:13:40.530 And there's a lot of danger in the war
00:13:43.770 right now in the world.
00:13:46.410 And there's a greatpossibility of World War III
00:13:49.710 and we better get this thing done fast
00:13:51.600 because five months withpeople like her and him,
00:13:57.870 he's checked out.
00:13:58.710 He just goes to the beach
00:13:59.850 and thinks he looksgood in a bathing suit,
00:14:02.370 which he doesn't.
00:14:04.170 He sort of checked out.
00:14:05.550 Hey look, you know, you can't blame him.
00:14:07.740 That was a coup. They took it over.
00:14:09.510 They took over the presidential deal.
00:14:14.430 The whole presidential thingwas taken over in a coup.
00:14:17.310 He had 14 million votes.He had no votes, not one.
00:14:22.080 And nobody thought it was gonna be her.
00:14:23.670 Nobody wanted it to be her.
00:14:25.110 She was a joke until sixweeks ago when they said,
00:14:30.720 politically, they feltthey had to pick her
00:14:34.110 and if they didn't pick her,
00:14:36.120 they thought they'd be a problem.
00:14:38.760 I don't know if that's right or not.
00:14:39.960 I actually don't think it's right.
00:14:41.340 But you know, they thought it was right.
00:14:44.010 And now immediately thepress comes to their aid.
00:14:47.970 If we can go back to China.
00:14:50.730 On negotiation, how do we avoid war
00:14:54.120 with China in the 21st century?
00:14:56.130 Well, there are ways,now here's the problem.
00:14:58.680 If I tell you how, and I'd love to do it,
00:15:02.550 but if I give you a plan,
00:15:04.770 like I have a very exacting plan
00:15:07.020 how to stop Ukraine and Russia.
00:15:10.350 And I have a certain idea,
00:15:12.780 maybe not a plan, but an idea for China.
00:15:15.420 Because we're in a lot of trouble.
00:15:19.230 They'll be in a lot of trouble too.
00:15:21.270 But we're in a lot of trouble.
00:15:23.580 But I can't give you those plans
00:15:25.200 because if I give you those plans,
00:15:26.670 I'm not gonna be able to use them.
00:15:27.780 They'll be very unsuccessful, you know,
00:15:29.820 part of it's surprise, right?
00:15:31.590 But they won't be able to help us much.
00:15:35.130 So you have a planof what to say to Putin
00:15:37.320 when you take office.
00:15:39.240 No, I had a very goodrelationship with him
00:15:41.280 and I had a good relationshipwith Zelenskyy too,
00:15:43.830 but had a very goodrelationship with Putin.
00:15:47.580 Tough topic, but important.You said, "Lost by whisker".
00:15:52.080 I'm an independent, Ihave a lot of friends
00:15:54.420 who are independent, manyof whom like your policies,
00:16:00.300 like the fact that you're a deal maker,
00:16:02.670 like the fact that you can end wars,
00:16:06.870 but they are troubled
00:16:09.570 by what happened in the 2020 election
00:16:12.450 and statements about widespread fraud
00:16:16.950 and this kind of stuff.
00:16:17.970 Fake elector scheme.
00:16:19.530 What can you say tothose independent voters
00:16:23.310 to help them decide who to vote for?
00:16:24.660 Right, I think the fraudwas on the other side.
00:16:26.820 I think the election was a fraud.
00:16:29.040 And many people felt it wasthat and they wanted answers.
00:16:34.920 And when you can't challenge an election,
00:16:37.320 you have to be able to challenge it.
00:16:38.670 Otherwise it's gonnaget worse. Not better.
00:16:42.630 And there are lots of waysto solve this problem.
00:16:45.510 Go to paper ballots, do it the easy way.
00:16:48.137 I mean the paper ballotsand you have voter ID
00:16:52.170 and you have same day voting
00:16:54.240 and you have proof of citizenship,which is very important
00:16:57.030 because we have peoplevoting that are not citizens.
00:16:59.910 They just came in and they'reloading up the payrolls,
00:17:04.530 they're loading up everything.
00:17:05.579 They're putting students in schools.
00:17:07.440 They don't speak a word of English.
00:17:09.690 And they're taking the seats of people
00:17:11.910 that are citizens of our country.
00:17:14.880 So look, we have
00:17:19.710 the worst border in thehistory of the world.
00:17:22.410 We have coming into our country right now,
00:17:24.599 millions and millions of people
00:17:26.670 at levels that nobody's ever seen.
00:17:28.319 I don't believe anycountry's ever seen it.
00:17:31.110 And they would use sticks and so stones
00:17:33.210 not to make it happen,not to let it happen.
00:17:35.610 We don't do anything.
00:17:37.200 And we have a personwho is the border czar
00:17:39.870 who now said she wasn'treally the border czar,
00:17:41.940 but she was the border czar,
00:17:43.110 but she was in charge of the border.
00:17:45.630 And we have her
00:17:47.610 and she's saying very strongly,"Oh, I did such a good job."
00:17:52.200 She was horrible, horrible.The harm she's done...
00:17:56.100 But we have people comingin from other countries
00:17:59.340 all over the world,not just South America.
00:18:01.680 And they're coming infrom prisons and jails.
00:18:04.230 They're coming in from mental institutions
00:18:06.840 and insane asylums andthey're street criminals
00:18:11.400 right off the street they take them
00:18:13.440 and they're being given to our country,
00:18:15.571 drug dealers, human traffickers.
00:18:19.320 We're destroying our country.
00:18:21.270 This is a sin what's beenallowed to take place
00:18:23.730 over the last four years.
00:18:24.870 We're destroying our country.
00:18:26.940 And we'll see how that all works out.
00:18:30.210 But it's not even believable.
00:18:32.790 And now you see, yousaw in Aurora, Colorado
00:18:37.920 a group of very toughyoung thugs from Venezuela
00:18:42.930 taking over big areas,including buildings.
00:18:46.860 They're taking over buildings.
00:18:48.030 They have their big rifles,
00:18:50.670 but they're taking over buildings.
00:18:52.650 We are not gonna let this happen.
00:18:54.450 We're not gonna let themdestroy our country.
00:18:57.090 And you know, in thosecountries crime is way down,
00:19:00.090 they're taking them outta their prisons,
00:19:01.740 which is good because good for them.
00:19:03.930 I do the same thing.
00:19:05.130 By the way, if I ranone of those countries,
00:19:06.870 any country in theworld, I would make sure
00:19:08.580 that America has everyone of our prisoners,
00:19:10.860 every one of our criminals would be here.
00:19:13.320 I can't believe they're goingso slowly, but some aren't.
00:19:16.650 And but they all are doing itand we can't let that happen.
00:19:21.330 They're emptying out their prisons
00:19:23.370 and their mental institutions
00:19:25.020 into the United States of America.
00:19:28.290 We can't let that happen.
00:19:29.940 So a lot of people believethat there was some shady stuff
00:19:32.910 that went on with the election,
00:19:34.680 whether it's media bias orbig tech, but still the claim
00:19:39.780 of widespread fraud is athing that bothers people.
00:19:42.750 Well, I don't focus on thepast, I focus on the future.
00:19:46.650 I mean, I talk abouthow bad the economy is,
00:19:48.570 how bad inflation is,
00:19:50.670 how bad things like, which is important.
00:19:54.510 Afghanistan was, in my opinion,the most embarrassing thing
00:19:58.650 that's ever happened to our country.
00:20:00.630 And because of that, I think when he said
00:20:03.360 how stupid we were, Putin went in,
00:20:06.870 but it was the most embarrassing moment
00:20:10.380 in the history of our country.
00:20:11.580 I really believe that.
00:20:13.560 But you know, we left 13 dead soldiers,
00:20:19.080 think of it, 13 dead soldiers,
00:20:21.210 many soldiers horrificallyhurt with arms and legs
00:20:24.180 and everything else gone.
00:20:27.270 We left hostages behind,we left Americans behind,
00:20:31.080 we left military equipment,
00:20:33.660 the likes of which nobody'sever left behind before.
00:20:36.630 Billions and billionsof dollars of equipment.
00:20:40.440 They're now selling the equipment.
00:20:41.730 They're one of the largestarms dealers in the world.
00:20:45.540 And very sad, very sad.
00:20:49.470 And, you know, we werethere for a long time.
00:20:52.740 I was going to get out, wewere getting ready to get out.
00:20:56.130 Then we got interrupted by the election,
00:20:58.380 but we would've been outwith dignity and strength.
00:21:02.370 We were having very little problem
00:21:03.810 with the Taliban when I was there
00:21:05.520 because they knew it was gonna be tough.
00:21:07.830 I dealt with Abdul.
00:21:09.360 Abdul was the leaderand we got along fine.
00:21:14.130 He understood, but youknow, they were shooting,
00:21:16.380 they were killing a lot ofour people before I came down.
00:21:19.440 And when I got there,I spoke to him, I said,
00:21:22.627 "Can't do it. Don't do it anymore."
00:21:24.870 We went 18 months before this happened,
00:21:28.200 this horrible day happened.
00:21:30.210 We went 18 months and nobodywas shot at or killed.
00:21:33.900 What do you think thatwas? The carrot or the stick?
00:21:35.730 In that case in Afghanistan?
00:21:36.990 The stick, definitely the stick.
00:21:38.510 So the threat of military force,
00:21:40.886 That was the stick, yeah,
00:21:42.046 it doesn't have to be,but that was the stick.
00:21:44.370 Well, let me just linger on the election
00:21:47.373 a little bit more.
00:21:48.210 For this election, itmight be a close one.
00:21:51.300 What can we do to avoid the insanity
00:21:53.850 and division of the previous election,
00:21:55.980 whether you win or lose?
00:21:58.020 Well, I hope it's not a close one.
00:21:59.610 I mean, you know, I don'tknow how people can vote
00:22:01.620 for somebody that hasdestroyed our country,
00:22:04.620 the inflation, the bad economy.
00:22:08.374 But to me in a way, theworst is what they've allowed
00:22:11.490 to happen at our border wherethey've allowed millions
00:22:13.890 of people to come in here from places
00:22:16.140 that you don't want to know about.
00:22:18.330 And I can't believe that that'sgonna be a close election.
00:22:21.120 You know, we're leading in the polls,
00:22:24.030 and it looks close,
00:22:25.800 but I think in the end it'snot gonna be a close election.
00:22:29.250 What do you think is the right way
00:22:30.120 to solve the immigration crisis?
00:22:32.010 Is mass deportation one of the solutions
00:22:34.890 you will think about?
00:22:35.723 Well you've gotta get thecriminals out of here fast.
00:22:38.700 You know, the peoplefrom mental institutions,
00:22:41.490 you gotta get them back intotheir mental institution.
00:22:44.040 No country can afford this.
00:22:45.420 You know, it's just too much money.
00:22:47.280 You look at what's happeningin New York and Chicago and LA
00:22:51.270 and lots of places and you takea look at what's happening.
00:22:54.960 There's no country can affordthis, we can't afford it.
00:22:58.320 And we've gotta get thebad ones out immediately
00:23:01.770 and the rest have to be worked on.
00:23:04.260 You know, it's happened before.
00:23:05.250 Dwight Eisenhower was sortof a moderate president,
00:23:08.970 moderate type person,
00:23:10.470 but he hated when he sawpeople pouring into the country
00:23:13.380 and they were, nothing like now.
00:23:15.840 You know, I probably got elected in 2016
00:23:18.630 because of the border
00:23:20.880 and I told people what washappening and they understood it.
00:23:23.670 And I won the election.
00:23:25.530 And I won the election Ithink because of the border.
00:23:27.990 Our border is 25 times worse right now
00:23:32.460 than it was in 2016.
00:23:35.400 I had it fixed too.
00:23:37.350 The last week of my, thefamous chart that I put up
00:23:41.700 was exactly that, you know, the chart.
00:23:44.670 When I looked to the right,I said there's the chart,
00:23:48.420 that was not a pleasant experience,
00:23:50.490 but the chart that I put up said,
00:23:52.407 and that was done by Border Patrol.
00:23:54.390 That was the lowest number
00:23:55.740 that we've ever had come into our country
00:23:57.660 in recorded history.
00:23:59.670 And we have to get it backto that again. We will.
00:24:04.020 Let me ask you about Project 2025.
00:24:06.150 So you've publicly said
00:24:06.983 that you don't have any directconnection to Project 2025?
00:24:09.180 Nothing. I know nothing about it.
00:24:11.430 And they know that too.Democrats know that.
00:24:13.887 And I purposely haven't read it
00:24:16.290 because I wanna say to you,
00:24:17.490 I have no idea what it's all about.
00:24:19.650 It's easier than saying I read it
00:24:22.170 and you know, all of the things.
00:24:23.580 No, I purposely haven't read it
00:24:26.490 and I've heard about it.
00:24:28.830 I've heard about things thatare in there that I don't like
00:24:32.640 and there's some things inthere that everybody would like.
00:24:35.520 But there are thingsthat I don't like at all.
00:24:39.900 And I think it's unfortunatethat they put it out,
00:24:44.670 but it doesn't mean anything
00:24:45.810 because it has nothing to do with me.
00:24:47.490 Project 25 has, it hasabsolutely nothing to do with me.
00:24:52.950 You posted recently about marijuana
00:24:55.440 and that you are okay
00:24:58.830 with it being legalized, butit has to be done safely.
00:25:01.740 Can you explain your policy there?
00:25:03.053 Well, I just put out a paper
00:25:05.640 and first of all, medicalmarijuana has been amazing.
00:25:11.010 I've had friends and I've had others
00:25:13.200 and doctors telling me thatit's been absolutely amazing,
00:25:17.580 the medical marijuana.
00:25:20.280 And we put out a statement that
00:25:24.780 we can live with the marijuana.
00:25:27.420 It's gotta be a certain age,
00:25:29.100 gotta be a certain age to buy it.
00:25:31.200 It's gotta be done in avery concerted, lawful way.
00:25:36.570 And the way they're doing it in Florida
00:25:39.030 I think is gonna be actually good.
00:25:41.130 It's gonna be very good,
00:25:42.780 but it's gotta be done in a good way.
00:25:44.610 It's gotta be done in a clean way.
00:25:46.500 You go into some of theseplaces, like in New York,
00:25:49.110 it smells all marijuana.
00:25:52.080 You've gotta have a systemwhere there's control.
00:25:55.500 And I think the way they'vedone it in Florida is very good.
00:25:59.280 Do you know anything about psychedelics?
00:26:01.320 So I'm not a drug guy, butI recently did ayahuasca.
00:26:06.051 And there's a lot of people
00:26:08.010 that speak to sort of the health benefits
00:26:11.430 and the spiritual benefits ofthese different psychedelics.
00:26:16.380 I think would probably have a better world
00:26:19.290 if everybody in Congresstook some mushrooms, perhaps.
00:26:23.370 Now I know you stay awayfrom all of that stuff.
00:26:27.990 I know also veterans useit for dealing with PTSD
00:26:30.867 and all that kind of stuff.
00:26:31.920 So it's great.
00:26:33.450 And it's interesting thatyou're thinking about
00:26:36.150 being more acceptingof some of these drugs
00:26:39.510 which don't just havea recreational purpose,
00:26:42.030 but a medical purpose,a treatment purpose.
00:26:44.940 So we put out a statement today,
00:26:46.710 we're gonna put out anotherone probably next week,
00:26:48.810 be more specific, althoughI think it's pretty specific
00:26:53.040 and we'll see how that all goes.
00:26:55.500 That's a referendumcoming up in some states,
00:26:59.430 but it's coming up andwe'll see how it does.
00:27:02.400 I will say it's been very hard to beat it.
00:27:06.660 You take a look at the numbers,
00:27:08.430 it's been very hard to beat it.
00:27:09.750 So I think it'll generally pass,
00:27:12.000 but you wanna do it in a safe way.
00:27:14.220 Speaking of marijuana,
00:27:15.480 let me ask you about mygood friend Joe Rogan.
00:27:18.510 So you had a bit of tension with him.
00:27:20.670 So when he said nice thingsabout RFK Jr, I think,
00:27:24.953 you've said some not sonice things about Joe
00:27:26.847 and I think that was a bit unfair.
00:27:29.460 And as a fan of Joe, I wouldlove to see you do his podcast
00:27:34.080 because he is legit
00:27:36.510 the greatest conversationalistin the world.
00:27:39.480 So what's the story behind the tension?
00:27:40.993 Well, I don't thinkthere was any tension.
00:27:43.590 And I've always liked him,
00:27:47.820 but I don't know him.
00:27:49.860 I only see him when I walkinto the arena with Dana
00:27:53.550 and I shake his hand.
00:27:55.110 I see him there and I thinkhe's good at what he does,
00:27:59.460 but I don't know about doing his podcast.
00:28:01.410 I mean, I guess I'd do it,but I haven't been asked
00:28:05.220 and I'm not asking them, youknow, I'm not asking anybody.
00:28:09.600 Sounds like a challengingnegotiation situation.
00:28:11.610 No, it's not really a negotiation.
00:28:14.460 And he's sort of a liberalguy I guess, you know,
00:28:17.280 from what I understand.
00:28:19.110 But he likes Kennedy.
00:28:20.490 This was before I found this out,
00:28:21.810 before Kennedy came in with us.
00:28:23.850 He's gonna be great.Bobby's gonna be great.
00:28:27.330 But I like that helikes Kennedy. I do too.
00:28:29.760 You know, he is a different kind of a guy,
00:28:31.890 but he's got some great things going
00:28:34.200 and I think he's gonna be...
00:28:37.320 Beyond politics, I think hecould be quite influential
00:28:40.980 in taking care of some situations
00:28:42.840 that you probably would agreeshould be taken care of.
00:28:45.750 The Joe Rogan post is an example.
00:28:47.760 I would love to get yourpsychology behind the tweets
00:28:52.140 and the posts on truth.
00:28:54.630 Are you sometimes beingintentionally provocative
00:28:57.210 or are you just speaking your mind
00:28:59.670 and are there times where you regret
00:29:02.190 some of the truths you've posted.
00:29:04.110 Yeah, I do. I mean, butnot that often, honestly.
00:29:06.930 You know, I do a lot of reposting.
00:29:09.870 The ones you get in troublewith are the reposts
00:29:12.090 because you find down deep,they're into some group
00:29:15.210 that you're not supposed to be reposting.
00:29:18.630 You don't even know if those groups
00:29:19.770 are good, bad or indifferent.
00:29:21.570 But the reposts are the onesthat really get you in trouble.
00:29:25.530 When you do your ownwords, it's sort of easier.
00:29:27.600 But the reposts go very quickly.
00:29:30.840 And if you're gonna checkevery single little symbol,
00:29:35.370 and I don't know, it's workedout pretty well for me.
00:29:39.360 I tell you, truth is very powerful.
00:29:44.880 And it's my platform
00:29:46.380 and it's been very powerful,very, very powerful.
00:29:49.410 It goes everywhere.
00:29:51.300 I call it my typewriter, you know,
00:29:52.980 that's actually my typewriter.
00:29:54.450 What are you doing usuallywhen you're composing a truth?
00:29:57.390 Like are you chilling back on a couch?
00:30:00.510 Couches, beds, lot of different things.
00:30:03.930 Like late at night and just...
00:30:05.817 I'd like to do some late at night.
00:30:07.440 You know, I'm not a huge sleeper.
00:30:09.780 But whenever I do them, youknow, past like three o'clock,
00:30:14.610 they criticize you the next day,
00:30:20.312 "Trump was truthing at threeo'clock in the morning."
00:30:23.460 And there should be no problem with that.
00:30:25.440 And then when you think abouttime zones, how do they know
00:30:27.600 that you are like, youknow, in a time zone,
00:30:30.150 like an Eastern zone?
00:30:32.880 But every time I do it after like two
00:30:34.800 or three o'clock, it'slike why is he doing that?
00:30:39.120 But it's gotten, I mean, you know,
00:30:42.810 the truth has become avery successful platform
00:30:49.680 and I like doing itand it goes everywhere.
00:30:52.020 As soon as I do it, it goes everywhere.
00:30:54.360 The country seemsmore divided than ever.
00:30:57.090 What can you do to helpalleviate some of that division?
00:30:59.490 Well, you can get ridof these two people.
00:31:01.290 They're terrible. They're terrible.
00:31:03.630 You don't want to havethem running this country.
00:31:05.610 They're not equipped to run it.
00:31:07.770 Joe, it's a disaster, okay?
00:31:12.780 And Kamala, I think she'llend up being worse than him.
00:31:17.100 We'll see, I think a lot's now, you know,
00:31:19.080 the convention's over with
00:31:21.180 and I see I'm leading injust about all the polls now.
00:31:24.720 They had their little honeymoonperiod as they call it.
00:31:28.350 And we'll see how thatall goes. Who knows.
00:31:31.680 From my personal opinion,I think you are at your best
00:31:35.610 when you're talking about apositive vision of the future
00:31:38.490 versus criticizing the other side.
00:31:40.950 Yeah, I think you haveto criticize though.
00:31:44.520 I think they're nasty.
00:31:46.770 They came up with astory that I looked down
00:31:50.910 and I called soldiersthat died in World War I
00:31:54.240 suckers and losers, okay?
00:31:56.820 Now number one, who would say that?
00:31:58.710 Number two, who would say itto military people? Nobody.
00:32:01.440 It was a made up story. Itwas just a made up story.
00:32:04.530 And they like to repeat it over again.
00:32:07.320 They know it was made up.
00:32:08.940 I have 26 witnesses that nothing was said.
00:32:13.770 They don't wanna hear about that.
00:32:16.500 Like she lied on McDonald's.
00:32:17.940 She said that she worked at McDonald's.
00:32:22.320 It's not a big lie, but it's a big lie.
00:32:25.110 I mean they just went and they checked
00:32:27.540 and unless she can showsomething they don't talk about,
00:32:30.180 the presses are gonna follow up with it.
00:32:31.740 But I'll keep hammering it,
00:32:34.200 but she never worked at McDonald's.
00:32:35.357 It was just a, you know,sort of a cool thing to say,
00:32:37.927 "Hey, I worked at McDonald's", you know.
00:32:41.880 But one of the worst was
00:32:43.890 two days ago I went to Arlingtonat the request of people
00:32:47.580 that lost their children.
00:32:50.460 They'll always bechildren to those people.
00:32:52.200 You understand that, that'snot politically incorrect
00:32:55.500 this thing to say.
00:32:56.850 The mother comes up, "I lost my child",
00:32:59.430 but you know, the child is the soldier.
00:33:02.550 And lost the child because of Biden
00:33:04.710 and because of Kamala
00:33:07.650 as just as though theyhad the gun in their hand
00:33:11.040 because it was so badly handled.
00:33:13.530 It should have been done at Bagram,
00:33:14.910 which is the big air base.
00:33:16.020 It shouldn't have been doneat a small little airport
00:33:18.780 right in the middle of townwhere people stormed it.
00:33:23.850 It was a true disaster.
00:33:27.750 And they asked me if I'dcome and celebrate with them.
00:33:34.379 Three years, they've died three years ago.
00:33:37.440 And I said, "I'm gonna try."
00:33:38.490 I got to know them because Ibrought them here, actually.
00:33:42.330 One night they almost all came here
00:33:46.500 and they said, "I wonder if Trump
00:33:47.700 will actually come and see us."
00:33:48.810 I heard they were here, I came, saw them.
00:33:50.460 We stayed for like four hours listening
00:33:52.530 to music up on a deckright upstairs, beautiful.
00:33:56.850 And they were great people.
00:33:57.990 So they called me overthe last couple of weeks
00:34:00.660 and they said, "We'regonna have a reunion,
00:34:03.060 our three year reunion,would you be able to come?"
00:34:05.880 And it was very hard forme to do it logistically,
00:34:08.520 but I said, "I'll get it done."
00:34:10.110 And I got there and wehad a beautiful time.
00:34:13.980 I didn't run away,
00:34:15.751 I didn't just walk in, shake hands
00:34:17.159 and walk out like people do.
00:34:19.590 And I wasn't looking at mywatch like Joe Biden does.
00:34:23.699 And it was amazing. So I did it for them.
00:34:27.449 I didn't do it for me. Idon't need the publicity.
00:34:30.570 I mean, I get more publicityprobably than anybody.
00:34:33.360 You would know that better than me.
00:34:34.679 But I think maybe more thananybody, maybe more than anybody
00:34:38.370 that's ever lived, I don't know.
00:34:40.739 But I don't think anyonecould have anymore.
00:34:42.449 Every time you turn on television,
00:34:44.100 there's like nine differentstories all on different topics
00:34:46.679 in the world about Trump.
00:34:48.000 As an example, youinterview a lot of people,
00:34:51.510 good people, successful people.
00:34:53.880 Let's see how you do with thisinterview versus them. Okay?
00:34:56.993 I mean, I can tell you right now
00:34:58.590 you're gonna get the highestnumbers you've ever had
00:35:00.780 by sometimes a factor of 10.
00:35:06.900 When a Gold Star
00:35:12.780 family asks me to come inand spend time with them,
00:35:17.460 and then they said, we did a ceremony.
00:35:20.640 And then we went down to the graves,
00:35:22.230 which was quite a distance away.
00:35:25.770 They said, "Sir, wouldyou come to the grave?"
00:35:29.160 And then they said, when we were there,
00:35:31.200 it's very sad actually
00:35:32.910 because these people shouldn't have died.
00:35:34.860 They shouldn't have died.
00:35:35.693 They died because of Bidenand because of Kamala.
00:35:39.600 They died because it just likeif they pulled the trigger,
00:35:42.360 okay, now I don't know ifthat's controversial to say,
00:35:45.390 but I don't think it is.
00:35:47.340 Afghanistan was the mostincompetently run operation
00:35:50.190 I think I've ever seen.
00:35:51.480 Military or otherwise,they were incompetent.
00:35:54.930 But the families askedme if I'd go, I did go.
00:35:59.160 Then the families said,
00:36:00.517 "Could we have a picture atthe tombstone of my son?"
00:36:03.780 And we did. Son or daughter.
00:36:06.060 There was a daughter too.
00:36:07.680 And I took numerouspictures with the families.
00:36:11.250 I don't know of anybody elsethat was in the pictures,
00:36:13.140 but there were mostlyfamilies I guess, that was it.
00:36:16.500 And then I left.
00:36:17.610 I spent a lot of time with them,
00:36:19.080 then I left and I get home that night
00:36:21.690 and I get a call that the Bidenadministration with Kamala
00:36:27.000 is accusing me of usingArlington for publicity.
00:36:32.730 Just the opposite. Just the opposite.
00:36:36.150 And actually did you see it just came out,
00:36:39.030 the families actually put out
00:36:40.350 a very strong statement defending me.
00:36:42.150 They said, "We asked them to be there."
00:36:44.880 Well, politicians and themedia can play those games.
00:36:47.550 And you're right, yourname gets a lot of views.
00:36:50.400 You're probably legit the mostfamous person in the world.
00:36:55.770 But on the previous thing,in the spirit of unity,
00:36:59.400 you used to be a Democrat.- Yeah.
00:37:01.920 Setting the politicians aside,
00:37:04.170 what do you respect mostabout people who lean left,
00:37:08.580 who are Democrats themselvesor of that persuasion,
00:37:12.210 progressives, liberals and so on?
00:37:15.150 Well, look, I respect thefact that everybody's in there
00:37:19.290 and you know, to a certain extent,
00:37:22.230 life is what you do whileyou're waiting to die,
00:37:24.870 so you might as well do a good job.
00:37:27.180 I think in terms of what'shappening now, I think, you know,
00:37:31.403 we have a chance to save the country.
00:37:33.450 This country's going down
00:37:35.790 and I called it with Venezuela,
00:37:37.230 I called it, with a lotof different countries.
00:37:39.750 And this country's going down.
00:37:41.730 If we don't win this election,
00:37:44.760 the election coming up on November 5th
00:37:48.840 is the most important electionthis country has ever had.
00:37:52.260 'Cause if we don't win it, I don't know
00:37:53.820 that there'll be another election
00:37:56.250 and it's gonna be acommunist country or close.
00:38:01.170 And there's a lot ofpeople listening to this,
00:38:03.060 myself included, that doesn't think
00:38:06.270 that Kamala is a communist.
00:38:09.480 Well, she's a Marxist.
00:38:11.070 Her father's a Marxist.- [Trump] That's right.
00:38:13.889 It's a little unusual, you know.
00:38:15.654 She's advocating for somepolicies that are towards
00:38:17.970 the direction of democraticsocialism, let's say.
00:38:22.500 But there's a lot of people
00:38:23.333 that kind of know the way government works
00:38:24.507 and they say, "Well none of those policies
00:38:26.400 are going to actually come to reality.
00:38:29.520 It's just being used duringthe campaign to, you know,
00:38:33.780 groceries are too expensive,we need them cheaper,
00:38:35.910 so let's talk about price controls.
00:38:37.950 And that's never gonna come to reality.
00:38:39.720 It could come to reality.
00:38:41.010 Look, I mean, she cameout with price control.
00:38:43.170 It's been tried like 121 different times
00:38:45.810 at different places over the years.
00:38:48.210 And it's never worked once.
00:38:49.500 It leads to communism,it leads to socialism,
00:38:53.730 it leads to having no food on the shelves
00:38:56.880 and it leads to tremendous inflation.
00:39:01.108 It's a bad idea.
00:39:02.280 Whenever we use termslike communism for her,
00:39:04.770 and I don't know if you know this,
00:39:06.090 but some people call you a fascist.
00:39:08.610 Yeah, they do.
00:39:09.630 So I figure it's all rightto call them a communist.
00:39:11.910 Yeah, they call me a lotworse than I call them.
00:39:13.683 They they do indeed.It's just sometimes...
00:39:16.380 It's interesting though,
00:39:17.213 they'll call me something that's terrible
00:39:18.480 and then I'll hit them back
00:39:20.550 and they'll say, "Isn't itterrible what Trump said?"
00:39:22.620 I said, "Well wait a minute,they just called me..."
00:39:24.990 So I believe you haveto fight fire with fire.
00:39:28.230 I believe they're very evilpeople. These are evil people.
00:39:31.920 You know, we have anenemy from the outside
00:39:35.310 and we have an enemy from within.
00:39:37.320 And in my opinion, the enemy from within
00:39:39.390 are radical left lunatics.
00:39:42.060 And I think you have to fight back.
00:39:44.040 Whenever there's a lotof fighting fire with fire,
00:39:47.730 it's too easy to forget thatthere's a middle of America
00:39:56.146 that's moderate and kind ofsees the good in both sides
00:39:59.730 and just likes one sidemore than the other
00:40:01.530 in terms of policies.
00:40:02.610 Like I said, there's a lot of people
00:40:03.870 that like your policies,that like your skill
00:40:07.080 in being able to negotiate and end wars
00:40:10.170 and they don't see the impendingdestruction of America.
00:40:14.760 You know, we had nowars when I was president.
00:40:17.730 That's a big thing. Not since78 years as that happened.
00:40:21.300 But we had no wars when I waspresident. We defeated ISIS.
00:40:24.360 But that was a war that was started
00:40:26.100 that we weren't anywhere near defeating.
00:40:29.130 But think of it, I had no wars.
00:40:30.480 And Viktor Orban, theprime minister of Hungary,
00:40:35.400 said, "The world has to have Trump back
00:40:37.560 because everybody was afraid of Trump."
00:40:39.270 Now that's what he said.
00:40:40.260 So I'm not using that term,but I think they respected me.
00:40:42.840 But he said China wasafraid. Russia was afraid.
00:40:45.720 Everybody was afraid.
00:40:47.580 And I don't care what wordthey use, it probably,
00:40:52.530 that's even a better wordif you wanna know the truth,
00:40:55.110 but let's use the word respect.
00:40:56.550 They had respect for me. Theyhad respect for the country.
00:41:00.120 I mean, I ended theNord Stream 2 pipeline,
00:41:02.910 the Russian pipeline.
00:41:04.800 Nobody else could have donethat. I ended it, it was done.
00:41:07.560 Then Biden comes in and he approved it.
00:41:11.040 So we're defending Germanyand these other countries
00:41:13.470 for peanuts compared to what it's worth.
00:41:17.190 And they're paying the personwe're defending them against
00:41:21.210 billions and billionsof dollars for energy.
00:41:24.210 I said, "How does that work?"
00:41:26.400 And we had it out with themand it worked out good.
00:41:28.410 And they paid hundredsof billions of dollars.
00:41:31.440 Or you wouldn't evenhave a NATO right now.
00:41:33.090 You wouldn't have NATOif it wasn't for me.
00:41:36.150 As the leader of the United States,
00:41:38.430 you were the mostpowerful man in the world,
00:41:41.040 as you mentioned, not only the most famous
00:41:42.840 but the most powerful.
00:41:44.010 And if you become leader again,
00:41:46.920 you'll have unprecedented power.
00:41:49.950 Just on your own personal psychology,
00:41:51.480 what does that power do to you?
00:41:53.040 Is there any threat of it corrupting
00:41:55.170 how you see the world?
00:41:56.280 No, I don't think so.
00:41:57.480 Look, I've been there for four years.
00:42:00.540 I could have done a bignumber on Hillary Clinton.
00:42:03.210 I thought it looked terribleto take the president's wife
00:42:06.060 and put her in prison.
00:42:08.520 She's so lucky I didn't doanything. She's so lucky.
00:42:13.410 Hillary is a lucky woman
00:42:15.090 because I had a lot ofpeople pushing me too.
00:42:20.033 They wanted to see something.
00:42:21.240 But I could have done something very bad.
00:42:24.570 I thought it looked so bad.
00:42:25.650 Think of it, you have thepresident of the United States
00:42:27.810 and you also had Secretaryof State, right, she was.
00:42:31.200 But you're gonna put thepresident's wife in prison?
00:42:34.470 And yet when I got out there, you know,
00:42:35.677 they have all thesehoaxes, they're all hoaxes,
00:42:39.060 but they have all these dishonest hoaxes
00:42:42.150 just like they did in the pastwith Russia, Russia, Russia.
00:42:45.360 That was a hoax.
00:42:46.950 The 51 different, youknow, agencies or agents,
00:42:51.570 that was a hoax.
00:42:53.040 The whole thing was a hoax.
00:42:55.222 There was so many hoaxes and scams,
00:43:00.660 but I didn't wanna puther in jail and I didn't.
00:43:03.810 And I explained it to people, you know,
00:43:05.280 they say lock her up, lock her up.
00:43:08.190 We won. I said, "We don'twanna put her in jail.
00:43:12.360 We wanna bring the country together.
00:43:13.830 I wanna bring the country together."
00:43:16.230 You don't bring the countrytogether by putting her in jail.
00:43:20.100 But then when I got out, youknow, they went to work on me.
00:43:23.160 It's amazing, and they suffer from
00:43:26.370 massive Trump Derangement Syndrome, TDS,
00:43:33.120 and I don't know if it'scurable from their standpoint.
00:43:36.960 A lot of people are very interested
00:43:38.400 in the footage of UFOs.
00:43:41.370 The Pentagon has released a few videos
00:43:45.840 and there's been anecdotalreports from fighter pilots.
00:43:49.400 So a lot of people wanna know,
00:43:50.820 will you help push the Pentagonto release more footage,
00:43:55.740 which a lot of people claim is available.
00:43:57.600 Oh yeah, sure, I'll dothat. I would do that.
00:43:59.760 I'd love to do that. I have to do that.
00:44:03.750 But they also are pushing me on Kennedy.
00:44:06.360 And I did release a lot,but I had people come to me
00:44:09.000 and beg me not to do it.
00:44:11.340 But I'll be doing that very early on.
00:44:14.400 Yeah, no, but I would do that.
00:44:16.590 There's a moment whereyou had some hesitation
00:44:19.170 about Epstein releasing someof the documents on Epstein.
00:44:21.870 Why the hesitation?
00:44:23.523 I don't think I had...
00:44:24.765 I mean, I'm not involved.
00:44:26.130 I never went to his island, fortunately.
00:44:31.590 But a lot of people did.
00:44:33.750 Why do you think so many smart,
00:44:35.430 powerful people allowedhim to get so close?
00:44:42.480 He was a good salesman.
00:44:44.876 He was a hailing hardy type of guy.
00:44:48.300 He had some nice assets thathe'd throw around like islands.
00:44:52.110 But a lot of big peoplewent to that island.
00:44:57.180 But fortunately I was not one of them.
00:44:59.790 It's just very strangefor a lot of people
00:45:01.890 that the list of clientsthat went to the island
00:45:05.700 has not been made public.
00:45:07.830 Yeah, it's very interesting isn't it?
00:45:11.400 Probably will be by the way. Probably.
00:45:13.560 So if you are able to, you'll be...
00:45:15.630 I'd certainly take a look at it.
00:45:17.400 Now, Kennedy's interesting'cause it's so many years ago.
00:45:21.120 You know, they do that for danger too,
00:45:23.220 because you know,endangers certain people,
00:45:25.470 et cetera, et cetera.
00:45:27.030 So Kennedy is very differentfrom the Epstein thing.
00:45:32.520 But yeah, I'd be inclinedto do the Epstein.
00:45:34.470 I'd have no problem with it.
00:45:36.300 That's great to hear.
00:45:37.530 What gives you strength whenyou're getting attacked?
00:45:39.630 You are one of the mostattacked people in the world.
00:45:43.500 I think you, you can't care that much.
00:45:47.310 I know people that careso much about everything,
00:45:49.650 like what people are saying,you can't care too much
00:45:53.160 because you end up choking.
00:45:55.620 One of the tragic thingsabout life is that it ends.
00:45:59.130 How often do you think about your death?
00:46:01.050 Are you afraid of it?
00:46:02.957 I have a friend who'svery, very successful
00:46:06.900 and he's in his 80s, mid 80s.
00:46:10.530 And he asked me that exact same question.
00:46:14.040 I turned it around. I said,"Well, what about you?"
00:46:16.710 He said, "I think about itevery minute of every day."
00:46:20.310 And then a week later, hecalled me to tell me something
00:46:23.730 and he starts off theconversation by going,
00:46:26.707 "Tick, tock, tick tock."
00:46:29.700 Yeah, this is a dark person,you know, in a sense.
00:46:32.880 But it is what it is.
00:46:36.030 I mean, you know, if you're religious,
00:46:39.450 you have I think abetter feeling toward it.
00:46:41.970 You know, you're supposed togo to heaven, ideally not hell,
00:46:45.750 but you're supposed togo to heaven if you good.
00:46:48.660 I think our country'smissing a lot of religion.
00:46:51.030 I think it really was a muchbetter place with religion.
00:46:55.140 It was almost a guide, you know,
00:46:56.490 to a certain extent it was a guide.
00:46:58.620 You want to be good to people.
00:47:00.300 Without religion, there's noreal, there are no guardrails.
00:47:04.920 I'd love to see us get back to religion,
00:47:07.350 more religion in this country.
00:47:09.690 Well, Mr. President, thank you
00:47:10.890 for putting yourself out there
00:47:11.910 and thank you for talking today.
00:47:13.290 Look, I love the country.
00:47:15.120 I wanna see the country be great
00:47:17.100 and we have a real chance at doing it,
00:47:18.630 but it's our last chance andI appreciate it very much.
00:47:22.710 Thank you.- Thank you.
00:47:24.990 Thanks for listeningto this conversation
00:47:26.550 with Donald Trump.
00:47:27.870 To support this podcast,
00:47:29.130 please check out oursponsors in the description.
00:47:31.950 And now, as I've started doing here
00:47:34.530 at the end of some episodes,
00:47:36.060 let me make a few commentsand answer a few questions.
00:47:39.060 If you would like to submit questions,
00:47:41.370 including in audio and video form,
00:47:43.410 go to lexfridman.com/ama
00:47:46.350 or get in touch with mefor whatever other reason
00:47:49.230 at lexfridman.com/contact.
00:47:52.110 I usually do this in a T-shirt,
00:47:53.850 but I figured for this episode,
00:47:55.620 I'll keep my suit and tie on.
00:47:58.260 So first, this might be a goodmoment to look back a bit.
00:48:02.070 I've been doing thispodcast for over six years,
00:48:04.920 and I first and foremosthave to say thank you.
00:48:09.120 I'm truly grateful for the support
00:48:11.130 and the love I've gotten along the way.
00:48:14.100 It's been, I would say,the most unlikely journey.
00:48:16.920 And on most days, I barely feellike I know what I'm doing.
00:48:20.460 But I wanted to talk a bit about
00:48:22.890 how I approach these conversations.
00:48:24.930 Now each conversation isits own unique puzzle.
00:48:27.840 So I can't speak generallyto how I approach these,
00:48:30.270 but here it may be useful to describe
00:48:32.100 how I approach conversationswith world leaders,
00:48:35.520 of which I hope to have many more
00:48:37.470 and do a better job every time.
00:48:40.050 I read a lot of history
00:48:42.120 and I admire the historian perspective.
00:48:44.970 As an example, I admire William Shirer,
00:48:47.520 the author of many books on Hitler,
00:48:49.440 including "The Rise andFall of the Third Reich".
00:48:53.040 He was there and lived through it
00:48:55.860 and covered it objectivelyto the degree that one could.
00:49:00.480 Academic historians, bythe way, criticize him
00:49:03.600 for being a poor historian
00:49:05.250 because he editorializeda little too much.
00:49:09.720 I think those same folkscriticized Dan Carlin
00:49:13.320 and his hardcore history podcast.
00:49:15.840 I respect their criticism,but I fundamentally disagree.
00:49:19.920 So in these conversationswith world leaders,
00:49:22.890 I try to put on my historian hat.
00:49:25.320 I think in the realm oftruth and public discourse,
00:49:27.990 there's a spectrum betweenthe ephemeral and the eternal.
00:49:32.610 The outrage mob and clickbait journalists
00:49:34.770 are often focused on the ephemeral,
00:49:37.500 the current thing, thecurrent viral shit stormer
00:49:41.160 of mockery and derision.
00:49:43.080 But when the battle of the day is done,
00:49:44.790 most of it will be forgotten.
00:49:47.400 A few true ideas will remain,
00:49:49.770 and those the historian hopes to capture.
00:49:53.010 Now, this is much easier said than done.
00:49:57.390 It's not just abouthaving the right ideals
00:49:59.460 and the integrity to stick by them.
00:50:01.560 It's not even just about havingthe actual skill of talking,
00:50:05.670 which I still think I suck at,
00:50:09.120 but let's say it's a work in progress.
00:50:12.600 You also have to make the scheduling work
00:50:14.730 and set up the entirety of the environment
00:50:17.280 in a way that is conduciveto such a conversation.
00:50:19.950 This is hard, really hard
00:50:21.900 with political and business leaders.
00:50:23.910 They are usually super busyand in some cases super nervous
00:50:27.630 because well, they've beenscrewed over so many times
00:50:31.650 with click bait, gotcha journalism.
00:50:33.840 So to convince them and their team
00:50:35.670 to talk for two, three,four, five hours is hard.
00:50:38.970 And I do think a good conversation
00:50:41.700 requires that kind of duration.
00:50:42.960 And I've been thinking a lot about why.
00:50:45.750 I don't think it's justabout needing the actual time
00:50:48.570 of three hours to cover all the content.
00:50:51.570 I think the longer form
00:50:53.610 with a hypotheticalskilled conversationalist,
00:50:57.270 relaxes things and allowspeople to go on tangents
00:51:00.600 and to banter about the details
00:51:03.420 because I think it's in the details
00:51:05.880 that the beautifulcomplexity of the person
00:51:07.620 is brought to light.
00:51:10.020 Anyway, I look forward totalking to more world leaders
00:51:13.440 and doing a better jobevery time as I said.
00:51:16.320 I would love to dointerviews with Kamala Harris
00:51:18.870 and some other politicalfigures on the left and right,
00:51:21.780 including Tim Walz, AOC,Bernie, Barack Obama,
00:51:25.920 Bill and Hillary,
00:51:27.300 and on the right, J.D Vance,Vivek, George. W and so on.
00:51:31.320 And on the topic of politics,let me say, as an immigrant,
00:51:35.670 I love this country, theUnited States of America.
00:51:38.700 I do believe it is thegreatest nation on earth,
00:51:41.700 and I'm grateful for the peopleon the left and the right
00:51:44.790 who step into the arena of politics
00:51:47.040 to fight for this country
00:51:48.690 that I do believe they all love as well.
00:51:52.440 I have reached out to Kamala Harris,
00:51:54.270 but not many of the others.
00:51:56.340 I probably should do a better job of that.
00:51:58.620 But I've been doing most ofthis myself, all the reach out,
00:52:01.079 scheduling, researchprep, recording and so on.
00:52:04.020 And on top of that,
00:52:05.370 I very much have been sufferingfrom imposter syndrome
00:52:08.220 with a voice in my headconstantly pointing out
00:52:10.140 when I'm doing a shitty job.
00:52:12.150 Plus a few folks graciouslyremind me on the internet,
00:52:17.100 the very same sentiment ofthis aforementioned voice.
00:52:21.900 All of this, while I have the option
00:52:23.580 of just hiding away atMIT, programming robots
00:52:25.860 and doing some cool AI researchwith a few grad students,
00:52:28.620 or maybe joining an AI company
00:52:30.510 or maybe starting my own,
00:52:32.190 all these options make me truly happy.
00:52:35.970 But like I said, most days Ibarely know what I'm doing,
00:52:38.730 so who knows what the future holds.
00:52:41.640 Most importantly, I'm forevergrateful for all of you
00:52:44.340 for your patience and your support
00:52:46.980 throughout this rollercoasterof the life I've been on.
00:52:49.830 I love you all.
00:52:51.960 Okay, now let me go onto some of the questions
00:52:55.050 that people had.
00:52:56.460 I was asked by a few people tocomment on Pavel Durov arrest
00:53:00.570 and on X being banned in Brazil.
00:53:03.570 Let me first briefly commenton the Durov of arrest.
00:53:07.110 So basic facts, PavelDurov is CEO of Telegram,
00:53:11.220 which is a messenger app
00:53:12.870 that has end-to-end encryption mode.
00:53:15.120 It's not on by default,
00:53:16.560 and most people don't usethe end-to-end encryption,
00:53:19.050 but some do.
00:53:20.940 Pavel was arrested in Franceon a long list of charges
00:53:25.350 related to quote unquote
00:53:26.827 "criminal activity carriedout on the Telegram platform"
00:53:31.050 and for quote unquote,
00:53:32.767 "providing unlicensed cryology services."
00:53:36.180 I think Telegram is indeedused for criminal activity
00:53:38.880 by a small minority ofits users, for example,
00:53:42.390 by terrorist groups to communicate.
00:53:45.060 And I think we all agreethat terrorism is bad.
00:53:47.880 But here's the problem,
00:53:49.380 as the old saying goes,
00:53:50.550 one man's terrorist isanother man's freedom fighter.
00:53:54.060 And there are many cases inwhich the world unilaterally
00:53:57.630 agrees who the terrorists are.
00:53:59.790 But there are othercases when governments,
00:54:02.700 especially authoritarianincline governments
00:54:05.250 tend to propagandize
00:54:06.900 and just call whoever's in the opposition,
00:54:09.330 whoever opposes them, terrorists.
00:54:11.640 There is some room for nuance here,
00:54:13.530 but to me at this time,
00:54:16.410 it seems to obviously bea power grab by government
00:54:19.950 wanting to have backdooraccess into every platform
00:54:23.310 so they can have censorshippower against the opposition.
00:54:26.550 I think generally governmentshould stay out of censoring
00:54:29.670 or even pressuring social media platforms.
00:54:33.090 And I think arrestinga CEO of a tech company
00:54:36.090 for the things said on theplatform he built is just nuts.
00:54:40.650 It has a chilling effect on him,
00:54:42.210 on people working at Telegram
00:54:44.250 and on people working atevery social media company
00:54:46.980 and also people thinking
00:54:48.210 of launching a new social media company.
00:54:50.490 Same as the case of Xbeing banned in Brazil.
00:54:54.000 It's I think a power grabby Alexandre de Moraes,
00:54:57.780 a Supreme Court justice in Brazil.
00:55:00.300 He ordered X to block certain accounts
00:55:02.460 that are spreading quoteunquote "misinformation".
00:55:05.880 Elon and X denied the request.
00:55:08.640 Then de Moraes threatened
00:55:10.740 to arrest X representatives in Brazil.
00:55:13.620 And in response to that, Xpulled the representatives
00:55:16.590 out of Brazil obviously to protect them.
00:55:19.950 And now X having norepresentatives in Brazil,
00:55:22.830 apparently violates the law.
00:55:24.660 Based on this de Moraesbanned X in Brazil.
00:55:28.770 Once again, it's an authoritarian figure
00:55:31.140 seeking censorship power overthe channels of communication.
00:55:34.800 I understand that this is complicated
00:55:37.260 because there are evil people in the world
00:55:39.510 and part of the role of government
00:55:40.980 is to protect us from those evil people.
00:55:43.680 But as Benjamin Franklin said,
00:55:46.110 those who can give up essential liberty
00:55:47.820 to obtain a little temporary safety
00:55:49.890 deserve neither liberty nor safety.
00:55:53.130 So it's a trade off, butI think in many places
00:55:55.920 in the world, many governmentshave leaned too far away
00:55:59.550 at this time from liberty.
00:56:02.100 Okay, next up I got a question on AI,
00:56:05.700 which I emotionally connected with.
00:56:08.400 I'll condense it as follows.
00:56:10.777 "Hello, Lex, I'm a programmer
00:56:13.830 and I have a deep fear ofslipping into irrelevance
00:56:17.040 because I am worried
00:56:18.180 that AI will soon exceedmy programming skills."
00:56:23.070 Let me first say thatI relate to your fear.
00:56:25.440 It's scary to have a thingthat gives you a career
00:56:28.140 and gives you meaning to be taken away.
00:56:30.810 For me, programming is a passion.
00:56:32.850 And if not for thispodcast, it would probably,
00:56:36.390 at least in part, be my profession.
00:56:38.280 So I get an uncomfortablefeeling every time Claude,
00:56:42.690 the LLMI use for coding at this time,
00:56:45.060 just writes a lot of excellent,
00:56:47.700 approximately correct code.
00:56:49.800 I think you can make a good case
00:56:51.210 that it already exceeds theskill of many programmers,
00:56:54.780 at least in the same way thatthe collective intelligence
00:56:57.180 of Stack Overflow exceeds theskill of many programmers,
00:57:00.780 many individual programmers.
00:57:02.010 But in many ways it still does not.
00:57:06.090 But I think eventually more and more
00:57:10.230 the professional programming will be one
00:57:12.720 of writing natural language prompts.
00:57:15.210 I think the right thing to do,
00:57:16.590 and what I'm at leastdoing is to ride the wave
00:57:21.300 of the ever improvingcode-generating LLMs,
00:57:24.030 and keep transforming myselfinto a big picture designer
00:57:27.450 versus low level tinkerer.
00:57:30.390 What I'm doing and what I recommend you do
00:57:33.390 is continually switch towhatever state of the art tool
00:57:36.060 is for generating code.
00:57:37.320 So for me, currently I recently switched
00:57:39.060 from VS Code to Cursor
00:57:41.190 and before that it wasEmacs to VS Code switch.
00:57:45.150 So Cursor is this editorthat's based on Vs Code
00:57:48.000 that leans heavily on LLMs
00:57:51.990 and integrates the codegeneration really nicely
00:57:54.660 into the editing process.
00:57:56.520 So it makes it super easyto continually use the LLMs.
00:58:01.530 So what I would advise
00:58:02.670 and what I'm trying to domyself is to learn how to use it
00:58:04.737 and to master its codegeneration capabilities.
00:58:08.340 I personally try to now allocate
00:58:10.920 a significant amount of time
00:58:12.540 to designing with natural language first
00:58:15.270 versus writing code from scratch.
00:58:17.430 So using my understanding of programming
00:58:22.170 to edit the code that'sgenerated by the LLM
00:58:24.960 versus sort of writing it from scratch
00:58:27.600 and then using the LLM togenerate small parts of the code.
00:58:30.570 I see it as a skill that I should develop
00:58:32.430 in parallel to my programming skill.
00:58:34.770 I think this applies tomany other careers too.
00:58:37.200 Don't compete with AI for your job,
00:58:39.720 learn to use the AI to do that job better.
00:58:43.080 But yes, it is scary on somedeep sort of human level,
00:58:49.470 the threat of being replaced,
00:58:51.810 but at least I think we'll be okay.
00:58:55.470 All right, next up I gota very nice audio message
00:58:58.650 and question from a gentleman who is 27
00:59:02.700 and feeling a lot ofanxiety about the future.
00:59:05.250 Just recently he graduatedwith a bachelor's degree
00:59:07.427 and he's thinking aboutgoing to grad school
00:59:09.540 for biomedical engineering,but there is a lot of anxiety.
00:59:13.140 He mentioned anxiety manytimes in the message.
00:59:16.440 It took him an extrawhile to get his degree,
00:59:18.150 so he mentioned he wouldbe 32 by the time he's done
00:59:22.020 with his PhD, so it's a big investment.
00:59:24.840 But he said in his heart hefeels like he's a scientist.
00:59:29.190 I think that's the most important part
00:59:30.660 of your message.
00:59:33.120 By the way, I'll figure outhow to best include audio
00:59:35.340 and video messages in future episodes.
00:59:37.800 Now onto the question.
00:59:39.690 So thank you for telling me your story
00:59:41.640 and for submitting the question.
00:59:43.680 My own life story is similar to yours.
00:59:45.810 I went to Drexel Universityfor my bachelor's, master's
00:59:49.740 and doctorate degrees
00:59:51.570 and I took a while just as you're doing.
00:59:55.620 I did a lot of non-standard things
00:59:57.810 that weren't any good forsome hypothetical career
01:00:01.110 I'm supposed to have.
01:00:02.640 I trained and competedin judo and jiujitsu
01:00:05.070 for my entire twenties,got a black belt from it.
01:00:10.050 I wrote a lot, including alot of really crappy poetry.
01:00:14.520 I read a large amount ofnon-technical books, history,
01:00:17.760 philosophy and literature.
01:00:19.920 I took courses onliterature and philosophy
01:00:21.690 that weren't at all requiredfor my computer science
01:00:24.690 and electrical engineering degrees.
01:00:26.760 Like a course on James Joyce.
01:00:29.220 I played guitar in bars around town.
01:00:32.790 I took a lot of technical classes,
01:00:34.980 many for example ontheoretical computer science
01:00:37.800 that were way more thanwere needed for the degree.
01:00:41.160 I did a lot of research
01:00:42.720 and I coded up a bunch of projects
01:00:44.430 that didn't directlycontribute to my dissertation.
01:00:49.050 It was pure curiosityand the joy of exploring.
01:00:53.640 So like you, I took thelong way home as they say,
01:00:58.830 and I regret none of it.
01:01:00.540 Throughout that people around me
01:01:02.040 and even people who loveme wanted me to hurry up
01:01:05.160 and to focus, especiallybecause I had very little money
01:01:08.490 and so I had a sense liketime was running out for me
01:01:13.830 to take the needed stepstowards a reasonable career.
01:01:18.390 And just like you, Iwas filled with anxiety
01:01:20.910 and I still am filledwith anxiety to this day,
01:01:24.630 but I think the right thingto do is not to run away
01:01:27.510 from the anxiety but to lean into it
01:01:29.550 and channel it into pursuingwith everything you got,
01:01:33.780 the things you're passionate about.
01:01:36.030 As you said, veryimportantly in your heart,
01:01:38.940 you know you're a scientist, so that's it.
01:01:41.580 You know exactly what to do.
01:01:43.320 Pursue the desire to be ascientist with everything you got.
01:01:47.040 Get to a good grad school,find a good advisor
01:01:50.430 and do epic shit with them.
01:01:53.460 And it may turn out in the end
01:01:54.990 that your life will haveunexpected chapters,
01:01:57.660 but as long as you'rechasing dreams and goals
01:01:59.820 with absolute unwavering dedication,
01:02:02.940 good stuff will come of it.
01:02:05.160 And also try your bestto be a good person.
01:02:08.640 This might be a good placeto read the words "If"
01:02:11.700 by Roger Kipling that I oftenreturn to when I feel lost
01:02:16.440 and I'm looking for guidanceon how to be a better man.
01:02:20.977 "If you can keep yourhead when all about you
01:02:23.160 are losing theirs and blaming it on you,
01:02:26.010 if you can trust yourselfwhen all men doubt you,
01:02:28.620 but make allowance for their doubting too.
01:02:31.110 If you can wait andnot be tired by waiting
01:02:33.570 or being lied about, don't deal in lies
01:02:36.300 or being hated, don't give way to hating
01:02:39.360 and yet don't look toogood nor talk too wise.
01:02:43.110 If you can dream and notmake dreams your master,
01:02:45.930 if you can think and notmake thoughts your aim.
01:02:48.780 If you can meet with triumph and disaster
01:02:51.540 and treat those twoimposters just the same.
01:02:54.750 If you can bear to hearthe truth you've spoken,
01:02:57.600 twisted by naves, theymake a trap for fools
01:03:01.230 or watch the things yougave your life to broken
01:03:04.770 and stoop and build themup with worn out tools.
01:03:08.760 If you can make one heapof all your winnings
01:03:11.640 and risk it on one turnof pitch and toss and lose
01:03:16.380 and start again at your beginnings
01:03:19.140 and never breathe a word about your loss.
01:03:22.380 If you can force yourheart to nerve and sin you
01:03:25.530 to serve your turn longafter they're gone.
01:03:29.220 And so hold on when there'snothing in you except the will,
01:03:33.600 which says to them, hold on.
01:03:36.720 If you can talk withcrowds and keep your virtue
01:03:39.570 or walk with kings orlose the common touch.
01:03:42.780 If neither foes, no lovingfriends can hurt you.
01:03:46.470 If all men count withyou, but none too much.
01:03:51.270 If you can fill the unforgivingminute with 60 seconds
01:03:55.140 worth of distance run, yours is the earth
01:03:58.770 and everything that's in it
01:04:00.390 and which is more,you'll be a man, my son."
01:04:05.460 Thank you for listeningand see you next time.


    
    """
    
    # Generate and print the results
    results = generate_topics(text)
    
    #print("Extracted Topics and Their Status:")
    #for result in results:
    #    print(result)

    #for result in results:
    #    print(f"\"{result['topic']}\", ")

    # Generate and print the summary
    summary = generate_summary(text)
    print("\nGenerated Summary:")
    print(summary)

    results = generate_topics(summary)
    print("Extracted Topics and Their Status:")
    for result in results:
        print(result)

if __name__ == '__main__':
    main()
