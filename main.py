class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def main(self):
        print(Solution.is_isogram(self, "Let's eat, Grandma!", 21))

    def is_isogram(self, text,key):
        aplhabet = "abcdefghijklmnopqrstuvwxyz"
        cipher = aplhabet[key:] + aplhabet[:key]
        result = ""
        for i in text:
            if i.isalpha():
                if i.isupper():
                    result += cipher[aplhabet.index(i.lower())].upper()
                else:
                    result += cipher[aplhabet.index(i)]
            else:
                    result += i
        return result


if __name__ == "__main__":
    Solution.main(object)
