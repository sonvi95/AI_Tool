from source.module.Cache.DiskCache import CACHE
from source.module.LLM.ModuleGrogAI import API_GROG
from source.module.AudioModule.ModuleSpeak import SPEAK


class Scenario:
    def __init__(self,configuration):
        self.configuration = configuration

    def get_introduce(self):
        """
        get introduce from the configuration
        :return:
        """
        print(self.configuration)
        key = self.configuration["Patient"]+self.configuration["Background"]
        rst = CACHE.get(key,{})
        if 'content' not in rst or 'mp4' not in rst or 'wav' not in rst:
            introduce = API_GROG.get_the_introduce(self.configuration)
            information_show = API_GROG.get_information_show(self.configuration)+'\n\n'
            file_output = SPEAK.create_video(introduce, CACHE.get_hash_value(key))
            CACHE.set(key, {'content':information_show,'mp4':file_output,'wav':file_output.replace('.mp4','.wav')})
            return  {'content':information_show,'mp4':file_output,'wav':file_output.replace('.mp4','.wav')}
        return rst

    def get_data_ice_phase(self):
        """
        get the data ice phase
        :return:
        """
        print(self.configuration)
        key = self.configuration['Patient']
        rst = CACHE.get(key,{})
        if 'content' not in rst or 'mp4' not in rst or 'wav' not in rst:
            data_speak = API_GROG.get_data_ice_phase(self.configuration['Patient'])
            file_output = SPEAK.create_video(data_speak, CACHE.get_hash_value(key))
            CACHE.set(key, {'content':data_speak,'mp4':file_output,'wav':file_output.replace('.mp4','.wav')})
            return  {'content':data_speak,'mp4':file_output,'wav':file_output.replace('.mp4','.wav')}
        return rst

    def start_convertation(self):
        """
        get start convert from the configuration
        :return:
        """
        print(self.configuration)
        key = self.configuration['Patient']+self.configuration['Background']+self.configuration['Person']
        rst = CACHE.get(key, {})
        if 'content' not in rst or 'mp4' not in rst or 'wav' not in rst:
            data_speak = API_GROG.get_sentence_to_start(self.configuration)
            file_output = SPEAK.create_video(data_speak, CACHE.get_hash_value(key))
            CACHE.set(key, {'content': data_speak, 'mp4': file_output, 'wav': file_output.replace('.mp4', '.wav')})
            return {'content': data_speak, 'mp4': file_output, 'wav': file_output.replace('.mp4', '.wav')}
        return rst

    def get_emotion(self):
        """
        get the emotion from the configuration
        :return:
        """
        print(self.configuration)
        key = self.configuration['Background']
        rst = CACHE.get(key, {})
        if 'content' not in rst or 'mp4' not in rst or 'wav' not in rst:
            data_speak = API_GROG.get_emotion_in_scenario(key)
            file_output = SPEAK.create_video(data_speak, CACHE.get_hash_value(key))
            CACHE.set(key, {'content':data_speak,'mp4':file_output,'wav':file_output.replace('.mp4','.wav')})
            return  {'content':data_speak,'mp4':file_output,'wav':file_output.replace('.mp4','.wav')}
        return rst

    def get_question(self):
        """
        get the request
        :return:
        """
        key = "Do you have any questions? If you dont have any questions please say NO."
        rst = CACHE.get(key, {})
        if 'content' not in rst or 'mp4' not in rst or 'wav' not in rst:
            file_output = SPEAK.create_video(key, CACHE.get_hash_value(key))
            CACHE.set(key, {'content':key,'mp4':file_output,'wav':file_output.replace('.mp4','.wav')})
            return file_output
        return rst

    def get_answer_for_question(self,question):
        """
        get the answer for the question
        :param question:
        :return:
        """
        key = "Answer"
        data_speak = API_GROG.get_answer_for_question(question,self.configuration['Patient'])
        file_output = SPEAK.create_video(data_speak, CACHE.get_hash_value(key))
        return {'content':'','mp4':file_output,'wav':file_output.replace('.mp4','.wav')}
