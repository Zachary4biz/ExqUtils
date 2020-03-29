def addStrings(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        i = len(num1) - 1
        j = len(num2) - 1
        result = ''
        carry = 0
        while i >= 0 or j >= 0:
            if i >= 0:
                carry += ord(num1[i]) - ord('0')
            if j >= 0:
                carry += ord(num2[j]) - ord('0')
            result += chr(carry % 10 + ord('0'))
            carry //= 10
            i -= 1
            j -= 1
        if carry == 1:
            result += '1'
        return result[::-1]

def addString(str1,str2):
    i = len(str1)-1
    j = len(str2)-1
    res = []
    c = 0
    while i >= 0 or j >= 0:
        if i>=0:
            c += ord(str1[i])-ord('0')
        if j>=0:
            c += ord(str2[j])-ord('0')
        res = [chr(c%10+ord('0'))]+res
        c = c // 10
        i -= 1
        j -= 1
    if c != 0:
        res = [chr(c + ord('0'))] + res
    return "".join(res)

print(addString("123","3"))
