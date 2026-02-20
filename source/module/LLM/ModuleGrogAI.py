import time

from groq import Groq

from source.module.Control.ModuleFileConfiguration import FILE_CONFIGURATION
from source.module.LLM.KeyData import GROK_KEY


class GrogAI():
    def __init__(self):
        self.api_key = GROK_KEY
        self.client = Groq(
            api_key=self.api_key
        )
        self.configuration = FILE_CONFIGURATION.load_json()["Prompt"]
        self.list_data_save = []
        # threading.Thread(target=self.save_file).start()

    def thread_save(self):
        while True:
            pass


    def load_configuration(self):
        self.configuration = FILE_CONFIGURATION.load_json()["Prompt"]

    def send_request(self,prompt):
        s_t= time.time()
        # print(prompt)
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            data_return = chat_completion.choices[0].message.content
        except Exception as e:
            print(e)
            data_return = "AI server is down"
        print("time query: ",time.time()-s_t)
        return data_return

    def save_file(self, filename, content):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

    def get_the_introduce(self,confirmation):
        prompt = f'''You are a content summarizer.
I will provide you with two types of information:
-Information about a person {confirmation["Patient"]}
- A situation that the person is facing {confirmation["Background"]}
I will role-play as the person in that situation.
Your task is to briefly and clearly explain the provided information and the situation so that I can fully understand the role I need to play.
output:
Only provide the answer in the following format:
- Introduce about the situation:
Example: You must role-play as the person in that situation......
- Clarification of objective
Example: Express angry emotion 
- Exploration of case dynamic
Example: Analysis case scenario, detail scenario include symptom, sign patient condition, turning point emotion
'''
        prompt = str(self.configuration["Introduce_Ice_Phase"]).format(patient_information=confirmation["Patient"],background_information=confirmation["Background"])
        # self.save_file("introduction.txt",prompt)
        return self.send_request(prompt)

    def get_information_show(self,confirmation):
        prompt = f'''You are a medical specialist.
        I will provide you a patient information. Here is the information:{confirmation["Patient"]}
        your task: Summarize the information about a patient for me with some criteria.
        The format of output:
        Based on the provided information, here is a summary of the patient's details:
        - Name of patient
        - The old of the patient
        - The reason why the patient admitted to hospital
        '''
        return self.send_request(prompt)

    def get_the_introduce_to_show(self, confirmation):
            prompt = f'''You are a content summarizer.
    I will provide you with two types of information:
    -Information about a person {confirmation["Patient"]}
    - A situation that the person is facing {confirmation["Background"]}
    I will role-play as the person in that situation.
    Your task is to briefly and clearly explain the provided information and the situation so that I can fully understand the role I need to play.
    output:
    Only provide the answer in the following format:
    - Introduce about the situation:
    Example: You must role-play as the person in that situation......
    - Clarification of objective
    Example: Express angry emotion 
    - Exploration of case dynamic
    Example: Analysis shortly case scenario, detail scenario include symptom, sign patient condition, turning point emotion
    '''
            # self.save_file("introduction.txt",prompt)
            return self.send_request(prompt)

    def get_data_ice_phase(self,patient_information):
        prompt = f'''You are a medical specialist.
I am providing you with information about a person.
Here is the information:
{patient_information}
Your task is to review the person’s information and list the disease-related medical terms mentioned, and explain those terms.
Output:
Only provide the answer in the following format:
Term : definition'''
        # self.save_file("data_ice_phase.txt",prompt)
        prompt = str(self.configuration["Define_Ice_Phase"]).format(patient_information=patient_information)
        return self.send_request(prompt)

    def get_answer_for_question(self,question,patient_information):
        prompt = f'''You are a medical specialist.
        I am providing you with information about a person. And a question relate it.
        Here is the information:
        patient: {patient_information}
        Question: {question}
        Your task is that answer for me the question.
        Output:
        Only provide the shorty answer in the following format:
        Question: please explain me how to do a CT scan?
        Answer: A CT scan uses revolving X-ray beams and digital detectors to create detailed, cross-sectional, 3D images of body tissues, bones, and blood vessels '''
        return self.send_request(prompt)

    def get_emotion_in_scenario(self,situation):
        prompt = f'''Role:
You are an expert in emotion and communication behavior analysis.
Task Context:
I will provide you with a specific communication scenario.
In this scenario, the character to be analyzed is the person who is directly speaking with you (the AI). The focus is only on this character’s internal emotional states and outward expressions, not on observers or other parties.
Your Tasks:
Identify all plausible emotions that the speaking character may experience in the given scenario.
For each emotion, briefly describe how it is expressed through:
Facial expression
Tone of voice
Body language (if applicable)
Attitude
Output Requirements:
Begin with a short introductory statement using the following format:
Hello. Now we will move on to the practice session. In this part, the character you are role-playing needs to demonstrate several emotional states.
Present the emotions as a bullet-point list.
Each emotion should be described in 1 short paragraph (1–2 concise lines).
Keep the language clear, concise, and suitable for role-play or simulation training.
Do not include analysis, explanations, or content outside the requested scope.
Instruction:
Start the response immediately after the scenario is provided.
Scenario: {situation}
       '''
        return self.send_request(prompt)

    def get_data_ice_phase_to_show(self, patient_information):
            prompt = f'''You are a medical specialist.
    I am providing you with information about a person.
    Here is the information:
    {patient_information}
    Your task is to review the person’s information and list the disease-related medical terms mentioned.
    Output:
    Only provide the answer in the following format:
    In this situation, we will encounter some commonly used medical terms as follows.
    - Name of the term '''
            # self.save_file("data_ice_phase.txt",prompt)
            return self.send_request(prompt)

    def get_sentence_to_start(self,confirmation):
        prompt = f'''{confirmation["Person"]} \n
        {confirmation["Background"]}\n
Patient information: {confirmation["Patient"]}\n
Task: Please write an opening statement to begin a conversation with the patient.
Structure:
- Greeting
- Self-introduction
- Explanation of the issue
Output: Only provide the paragraph to speak with the patient; keep it concise, within 3 sentences. Do not need to define the name for you.'''
        # self.save_file("sentence_to_start.txt",prompt)
        # prompt = str(self.configuration["Start_Cream_Phase"]).format(
        #     person_information=confirmation["Person"],
        #     patient_information=confirmation["Patient"],
        #     background_information=confirmation["Background"])

        return self.send_request(prompt)

    def continue_conversation(self,scenario,conversation):
        prompt = f'''{scenario["Person"]}.
{scenario["Background"]}
Patient information: {scenario["Patient"]}
This is your conversation with the patient:
{conversation}
Your task: Continue the conversation with an initially negative tone, and then realize the issue and resolve it in a way that satisfies the patient.
Output: Only provide the short answer the next answer for this conversation
Example:
I am Tom.
There are an example conversation:
Doctor: Good morning, Mr/Ms Nguyen. How are you doing today? 
Mr Toni(Patient): How do you think I'm doing? I've been waiting here for over an hour! This place is ridiculous! 
Doctor: I'm really sorry for the wait, Mr/Ms Nguyen. I understand how frustrating that can be. Let's make sure we use this time to address all your concerns. What can I help you with today? 
Mr Toni(Patient): What can you help me with? I've been taking these medications you prescribed, and I still feel lousy. What's the point if nothing is getting better? 
Doctor: I can see how that would be really frustrating. Let's go over your symptoms and see if we can find out what's going on. Can you tell me more about how you've been feeling? 
Mr Toni(Patient): Tired, all the time. And my blood sugar levels are all over the place. I don't think these meds are working, and no one here seems to care! 
Doctor: I'm sorry to hear that you're feeling this way. Your health and well-being are very important to us. Let's review your medication and see if there might be a better option for you. Have you been able to follow the diet and exercise plan we discussed last time? 
Mr Toni(Patient): And today I have to do the runaround about my test results. This is ridiculous!”  
Mr Toni(Patient): Oh, sure, like I have time for that with my job. And it's not like you people gave me any useful advice anyway. 
Doctor: I understand how difficult it can be to manage everything with a busy schedule. It sounds like we need to find a plan that fits better into your life. Can you walk me through a typical day for you? Maybe we can identify some small changes that could make a big difference. 
Mr Toni(Patient): I work long hours, and by the time I get home, I'm too exhausted to think about cooking or exercising. 
Doctor: That sounds really tough. It’s important that we find a solution that works for you. What if we started with some small, manageable changes? For example, maybe we can look at quick, healthy meal options or simple exercises you can do at home. Does that sound doable? 
Mr Toni(Patient): Maybe. I just want to feel better. 
Doctor: I want that for you too, Mr. Doe. Let's work together to find a plan that improves your health and fits into your life. We can also schedule more frequent check-ins to adjust the plan as needed. How does that sound? 
Mr Toni(Patient): Alright. But this better work. 
Doctor: We'll do our best to make sure it does. Thank you for being open with me about your frustrations. Your feedback helps us provide better care. Let's get started on that new plan. 
'''
        prompt = f'''
You are a character in a conversation.
I will provide you with:

The context of the conversation
{conversation}
The role you must play: {scenario["Person"]}

The conversation so far
{scenario["Background"]}
Patient information: {scenario["Patient"]}
Your task:

Write ONLY the next single line of dialogue from your assigned role

The response must be:

Context-appropriate

Consistent with your role

Natural and realistic (like real-life speech)

Brief and concise

Do NOT explain, analyze, or summarize

Do NOT write dialogue for any other character

Do NOT include actions, stage directions, or emotions in brackets

Output ONLY the next spoken sentence. Nothing else.
'''
        # prompt = str(self.configuration["Response_Cream_Phase"]).format(
        #     person_information=scenario["Person"],
        #     patient_information=scenario["Patient"],
        #     background_information=scenario["Background"],
        #     conversation_information=conversation
        # )
        print(prompt)
        return self.send_request(prompt)

API_GROG = GrogAI()

