import json


class DataBase:
    data = None

    def __init__(self):
        with open("Database/channels.json", 'r') as _:
            self.data = json.load(_)

    def enableBlock(self, chatId: str, channelId: str, inviteLink: str):
        try:
            self.data[chatId].append({'id': channelId, 'link': inviteLink})
            print(self.data)
        except:
            self.data[chatId] = [{'id': channelId, 'link': inviteLink}]
        self.__save()

    def disableBlock(self, chatId: str):
        try:
            self.data[chatId] = []
            self.__save()
        except:
            pass

    def getId(self, chatId: str):
        return [id['id'] for id in self.data[chatId]]

    def getInvLink(self, chatId: str, channelId: str):
        return [_['link'] for _ in self.data[chatId] if _['id'] == channelId].pop()

    def __save(self):
        with open('Database/channels.json', 'w') as _:
            json.dump(self.data, _)
