#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################################
#                                                                                   #       
# pyglut an pyopengl utilities module with severals 3D programming                  #
# helper class and functions.                                                       #
# Copyright (C) 2014 Brüggemann Eddie alias mrcyberfighter.                         #
#                                                                                   #
# This file is part of the pyglut module.                                           #
# pyglut is free software: you can redistribute it and/or modify                    #
# it under the terms of the GNU General Public License as published by              #
# the Free Software Foundation, either version 3 of the License, or                 #
# (at your option) any later version.                                               #
#                                                                                   #
# pyglut is distributed in the hope that it will be useful,                         #  
# but WITHOUT ANY WARRANTY; without even the implied warranty of                    # 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                      #
# GNU General Public License for more details.                                      #
#                                                                                   #
# You should have received a copy of the GNU General Public License                 #
# along with pyglut. If not, see <http://www.gnu.org/licenses/>                     #
#                                                                                   #
#####################################################################################


class Color(object) :
  def __init__(self,ub_v=False,f_v=False) :
    ''' Class for the color management:
        The color can be encoded as unsigned byte or as float.
        With type conversion methods and sequences returning getters.
    '''
        
    if not isinstance(ub_v,bool) :
      # Color given as unsigned byte vector.
      if len(ub_v) >= 3 :
        
        if ub_v[0] >= 0 and ub_v[0] <= 255 and not isinstance(ub_v[0],float) :
          self.r=ub_v[0] ;
        else :
          raise ValueError(0,255)
            
        if ub_v[1] >= 0 and ub_v[1] <= 255 and not isinstance(ub_v[1],float) :  
          self.g=ub_v[1] ;
        else :
          raise ValueError(0,255)
        
        if ub_v[2] >= 0 and ub_v[2] <= 255 and not isinstance(ub_v[2],float) :
          self.b=ub_v[2] ;
        else :
          raise ValueError(0,255)
          
        if len(ub_v) == 4 :
          # The alpha value is given.
          if ub_v[3] >= 0 and ub_v[3] <= 255 and not isinstance(ub_v[3],float) :
            self.a=ub_v[3] ;
          else :
            raise ValueError(0,255)  
        
        else :
          self.a=False ;
        
        self.encoding="ub" ;
        
        return 
        
      else :
        raise ValueError(ub_v,list,tuple,len(ub_v))  
      
    elif not isinstance(f_v,bool) :
      # Color given as an float vector.
      if len(f_v) >= 3 :
      
        if f_v[0] >= 0. and f_v[0] <= 1. :
          self.r=f_v[0] ;
        else :
          raise ValueError(0.0,1.0)
                
        if f_v[1] >= 0. and f_v[1] <= 1. :  
          self.g=f_v[1] ;
        else :
          raise ValueError(0.0,1.0)
            
        if f_v[2] >= 0. and f_v[2] <= 1. :  
          self.b=f_v[2] ;
        else :
          raise ValueError(0.0,1.0)
          
        if len(f_v) == 4 :
          # The alpha value is given.
          if f_v[3] >= 0. and f_v[3] <= 1. : 
            self.a=f_v[3] ;
          else :
            raise ValueError(0.0,1.0)  
        
        else :
          self.f_a=False ;
        
        self.encoding="float" ;
        
        return
        
      else :
        raise ValueError(f_v,list,tuple,len(f_v))    
  
  
    else :
      self.r=0
      self.g=0
      self.b=0
      self.a=0
      return None
  
  def get_float_v(self) :
    ''' Return the color as an sequence of floats '''
      
    if self.encoding == "ub" :  
      self.r=self.r/255. ;
      self.g=self.g/255. ;
      self.b=self.b/255. ;
      if not isinstance(self.a,bool) :  
	self.a=self.a/255. ; 
      
      self.encoding="float" ;
      
    if not isinstance(self.a,bool) :
      return (self.r,self.g,self.b,self.a)
    else :
      return (self.r,self.g,self.b)
  
  def get_ubyte_v(self) :
    ''' Return the color as an sequence of unsigned byte '''
    
    if self.encoding == "float" :
      self.r=int(self.r*255.) ;
      self.g=int(self.g*255.) ;
      self.b=int(self.b*255.) ;
      if not isinstance(self.a,bool) :   
	self.a=int(self.a*255.) ;
    
      self.encoding="ub" ;
    
    if not isinstance(self.a,bool)  :
      return (self.r,self.g,self.b,self.a)
    else :
      return (self.r,self.g,self.b)
    
  def set_in_float_values(self) :
    ''' Convert unsigned byte encoded color in floats values. '''
    
    if not self.encoding == "float" :
      self.r=self.r/255. ;
      self.g=self.g/255. ;
      self.b=self.b/255. ;
      if not isinstance(self.a,bool) :   
        self.a=self.a/255. ;
        
      self.encoding="float" ;
  
  def set_in_ub_values(self) :
    ''' Convert float encoded color in unsigned byte values. '''
    
    if not self.encoding == "ub" :
      self.r=int(self.r*255.) ;
      self.g=int(self.g*255.) ;
      self.b=int(self.b*255.) ;
      if not isinstance(self.a,bool) :
        self.a=int(self.a*255.) ;
        
      self.encoding="ub" ;
    
  def __doc__(self) :
    ''' Print documentation '''
    print '''
    Colors management class implementing an
    <type 'Color'> datatype.
    The Color can be initialize with an sequence from:
    -> unsigned byte color encoding: values == [0-255].
    -> float color encoding        : values == [0.0-1.0]. 
    with the keywords: ub_v (unsigned bytes vector).
			f_v  (floats vector).
	
    The Color class implement color encoding conversion methods:
    
    -> set_in_float_values() 
      Convert an unsigned byte encoded color in an float encoding.
    
    -> set_in_ub_values()
      Convert an float encoded color in an unsigned byte encoding.
    
    The current encoding can be retrieve thruoght the value of the attribute:
    
      Color.encoding
      
    And the color value can be retrieve as an 3 or 4 items sequence (vector),
    throught the methods:
    
    -> get_ubyte_v() Return the color as an sequence of unsigned byte.
    
    -> get_float_v() Return the color as an sequence of floats 
    
    or individually throught the attributes:
    
    Color.r (Red).
    Color.g (Green).
    Color.b (Blue).
    Color.a (Alpha).
    '''