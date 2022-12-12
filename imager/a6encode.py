"""
Steganography methods for the imager application.

This module provides all of the test processing operations (encode, decode) 
that are called by the application. Note that this class is a subclass of Filter. 
This allows us to layer this functionality on top of the Instagram-filters, 
providing this functionality in one application.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Authors: Jephthah Kwame Mensah (jkm255) & Aboagye Alfred (ana58)
Date: November 15th, 2022
"""
import a6filter

class Encoder(a6filter.Filter):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of Filter.  That means it inherits all of the 
    methods and attributes of that class too. We do that separate the 
    steganography methods from the image filter methods, making the code
    easier to read.
    
    Both the `encode` and `decode` methods should work with the most recent
    image in the edit history.
    """
    
    def encode(self, text):
        """
        Returns True if it could hide the text; False otherwise.
        
        This method attemps to hide the given message text in the current 
        image. This method first converts the text to a byte list using the 
        encode() method in string to use UTF-8 representation:
            
            blist = list(text.encode('utf-8'))
        
        This allows the encode method to support all text, including emoji.
        
        If the text UTF-8 encoding requires more than 999999 bytes or the 
        picture does  not have enough pixels to store these bytes this method
        returns False without storing the message. However, if the number of
        bytes is both less than 1000000 and less than (# pixels - 10), then 
        the encoding should succeed.  So this method uses no more than 10
        pixels to store additional encoding information.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns True...)
        # The last paragraph (If the text UTF-8 encoding...)
        # The precondition (text is a string)
        assert type(text) == str, repr(text) + ' is not a string'

        current = self.getCurrent()
        blist = list(text.encode('utf-8'))
        msg_length = len(blist)

        if msg_length > 999999 or len(blist)> len(current):
            return False
        
        if msg_length < 1000000 and len(blist) < (len(current) - 10):
            rgb = self._encode_pixel(0, 300, current)
            current[0] = rgb

            ind = 2
            for pos in range(0, msg_length):
                rgb = self._encode_pixel(pos+2, blist[pos], current)
                current[pos+2] = rgb
                ind += 1
            rgb = self._encode_pixel(ind, 400, current)
            current[ind] = rgb
            
            rgb = self._encode_pixel(1, ind, current )
            current[1] = rgb
            
            return True
        
    def decode(self):
        """
        Returns the secret message (a string) stored in the current image. 
        
        The message should be decoded as a list of bytes. Assuming that a list
        blist has only bytes (ints in 0.255), you can turn it into a string
        using UTF-8 with the decode method:
            
            text = bytes(blist).decode('utf-8')
        
        If no message is detected, or if there is an error in decoding the
        message, this method returns None
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns the secret...)
        # The last paragraph (If no message is detected...)

        current = self.getCurrent()
        blist = []
        ind = self._decode_pixel(1)

        if self._decode_pixel(0) == 300 and self._decode_pixel(ind) == 400:
            for pos in range(2, ind):
                blist.append(self._decode_pixel(pos))
        else:
            return None

        try:
            text = bytes(blist).decode('utf-8')
        except Exception:
            return None
        
        return text
    
    # HELPER METHODS
    def _decode_pixel(self, pos):
        """
        Return: the number n hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as 
        the last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        # This is helper. You do not have to use it. You are allowed to change it.
        # There are no restrictions on how you can change it.
        rgb = self.getCurrent()[pos]
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        num = (red % 10) * 100  +  (green % 10) * 10  +  blue % 10
        return num

    def _encode_pixel(self, pos, n, current):
        """
        Return: a pixel obtained from encoding a number n into a pixel
        at position pos in the current image.
        
        This function assumes that the number n is a 3-digit number encoded
        as the last digit in each color channel (e.g. red, green and blue).

        Take the last digits of the red, green and blue color values
        in the pixel at position pos and respectively replace them with
        the first, second, and third digits of the number n 

        If the resulting color value for red, green, or blue is 
        more than 255, subtract 10 from that resulting color value.

        The final resulting color values for red, green, and blue should
        be in the range 0(inclusive) to 255(inclusive). 
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)

        Parameter n: a number to be hidden
        Precondition: n is a 3-digit integer
        """
        rgb = current[pos]
        red = rgb[0] + n//100 - rgb[0]%100%10
        green = rgb[1] + (n%100)//10 - rgb[1]%100%10
        blue = rgb[2] + (n%100%10)//1 - rgb[2]%100%10

        if red > 255:
            red -=10
        if green > 255:
            green -= 10
        if blue > 255:
            blue -= 10
        
        rgb = (red, green, blue)

        return rgb
