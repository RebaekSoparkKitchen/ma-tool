'''
@Description: 
@Author: FlyingRedPig
@Date: 2020-11-23 18:08:28
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-23 18:56:28
'''


class Similarity():

    @staticmethod
    def compare(str1: str, str2: str):
        """
        campare the similarity of two strings
        """
        # ignore lower and capital letters
        str1 = str1.lower()
        str2 = str2.lower()
        l1 = list(str1)
        l2 = list(str2)
        intersection = list(set(l1).intersection(set(l2)))
        union = list(set(l1).union((set(l2))))

        return len(intersection) / len(union)

if __name__ == "__main__":
    print(Similarity.compare('claire zhou','zhou tiger'))

        
