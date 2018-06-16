#!/usr/bin/python3
import sys
import math
class VarintEncode:

   def __init__(self): 
       print("===============")

   def getEndian(self):
       num = 0x12345678
       res = num&0xff
       if(res==0x78):
           print("little-endian")
       else:
           print("big-endian")


   def decode(self, in_bytes):

       length = len(in_bytes)

       if(length<=0):
           return None 

       i = 0
       number = 0
       while(in_bytes[i]&0x80 != 0):
           number  = number | ((in_bytes[i] & 0x7f )<< (7*i))
           i += 1

       number  = number | (in_bytes[i]  << (7*i))

       in_bytes = number.to_bytes(i+1, byteorder='little', signed=True) 
       res_bytearraystr = ' '.join([bin(b) for b in in_bytes])
       print("decode[%s] is:\t %s " %(i+1,res_bytearraystr))
       print("decode number:\t %s" %number)

       cell = number % 2
       if(cell==0):
           number = number >>1
       else:
           number = ((number+0x01) >>1)*-1 
           #number = round((number + 1) /2 * -1)  # round method and division (/) is wrong when the number is too big ( Negative or Positive) 
       return number

   def isNumber(self,x):
       try:
           x=int(x)
           return isinstance(x,int)
       except ValueError:
           return False

   def encode(self, in_number_):


       # lenint = 16bytes base info + length of int
       lenint  = sys.getsizeof(in_number_)

       
       #负数右移高位补1，正数右移高位补0；负数、正数左移低位补0。
       #if(in_number_ < 0):
       #    in_number = -1*in_number_*2 -1 
       #else:
       #    in_number = in_number_ * 2
       in_number = (in_number_<<1)^(in_number_>>(lenint*8-1))
         
        

       print("convert num is:\t%s\nbin[%s] is:\t%s" %(in_number,sys.getsizeof(in_number),bin(in_number))); # bin(num): the output string is big-endian. but the number in memory is little endian.


       lenint = lenint + math.ceil(lenint/8) 
       res_bytearray = bytearray(lenint) #  use  little-endian for varint encoding
       
       count = 0 
       while(in_number >= 128 ):
           res_bytearray[count] = 0x80 | (in_number & 0x7f) 
           count += 1
           in_number = in_number >> 7
       res_bytearray[count] = 0x00 | (in_number & 0x7f) 
       count += 1

       res_bytearray = res_bytearray[0 : count]
       res_bytearraystr = ' '.join([bin(b) for b in res_bytearray])
       
       print("encode[%s] is:\t%s" %(count,res_bytearraystr) )
       return res_bytearray;
       
       

        
          
      
if(__name__=="__main__"):
    varint = VarintEncode();
    while(1):
        number = input("pls input a number: ")   
        if(not varint.isNumber(number) ):
          print("Bye!")
          break; 
        number = int(number)
        res = varint.encode(number)
        ans = varint.decode(res)
        print("decode is:\t%s \n============\n" %ans)
