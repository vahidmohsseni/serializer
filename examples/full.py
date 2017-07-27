# -*- coding: utf-8 -*-

# python imports
import struct
from enum import Enum


class EColor(Enum):
	white = 0
	red = 3
	green = 4
	blue = -2
	black = -1


class Parent1(object):

	def __init__(self, init=False):
		super(Parent1, self).__init__()
	
		if init:
			self.initialize()
		else:
			self.p1 = None
	

	def initialize(self):
		self.p1 = int()
	

	def serialize(self):
		s = b''
		
		# serialize self.p1
		s += struct.pack('I', self.p1)
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize self.p1
		self.p1 = struct.unpack('I', s[offset:offset + 4])[0]
		offset += 4
		
		return offset


class Parent2(object):

	def __init__(self, init=False):
		super(Parent2, self).__init__()
	
		if init:
			self.initialize()
		else:
			self.p2 = None
	

	def initialize(self):
		self.p2 = int()
	

	def serialize(self):
		s = b''
		
		# serialize self.p2
		s += struct.pack('q', self.p2)
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize self.p2
		self.p2 = struct.unpack('q', s[offset:offset + 8])[0]
		offset += 8
		
		return offset


class Child(Parent1, Parent2):

	def __init__(self, init=False):
		super(Child, self).__init__()
	
		if init:
			self.initialize()
		else:
			self.c = None
	

	def initialize(self):
		Parent1.initialize(self)
		Parent2.initialize(self)
		
		self.c = str()
	

	def serialize(self):
		s = b''
		
		# serialize parents
		s += Parent1.serialize(self)
		s += Parent2.serialize(self)
		
		# serialize self.c
		tmp0 = b''
		tmp0 += struct.pack('I', len(self.c))
		while len(tmp0) and tmp0[-1] == b'\x00'[0]:
			tmp0 = tmp0[:-1]
		s += struct.pack('B', len(tmp0))
		s += tmp0
		
		s += self.c.encode('ascii')
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize parents
		offset = Parent1.deserialize(self, s, offset)
		offset = Parent2.deserialize(self, s, offset)
		
		# deserialize self.c
		tmp1 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		tmp2 = s[offset:offset + tmp1]
		offset += tmp1
		tmp2 += b'\x00' * (4 - tmp1)
		tmp3 = struct.unpack('I', tmp2)[0]
		
		self.c = s[offset:offset + tmp3].decode('utf-8')
		offset += tmp3
		
		return offset


class Test(object):

	def __init__(self, init=False):
		super(Test, self).__init__()
	
		if init:
			self.initialize()
		else:
			self.v0 = None
			self.v1 = None
			self.v10 = None
			self.v11 = None
			self.v12 = None
			self.v13 = None
			self.v14 = None
			self.v15 = None
			self.v16 = None
			self.v17 = None
			self.v18 = None
			self.v19 = None
			self.v2 = None
			self.v20 = None
			self.v3 = None
			self.v4 = None
			self.v5 = None
			self.v6 = None
			self.v7 = None
			self.v8 = None
			self.v9 = None
	

	def initialize(self):
		self.v0 = bool()
		self.v1 = '\x00'
		self.v10 = float()
		self.v11 = int()
		self.v12 = str()
		self.v13 = list(EColor)[0]
		self.v14 = Child()
		self.v15 = list()
		self.v16 = list()
		self.v17 = dict()
		self.v18 = dict()
		self.v19 = [int() for _ in range(10)]
		self.v2 = int()
		self.v20 = [[list() for _ in range(20)] for _ in range(10)]
		self.v3 = int()
		self.v4 = int()
		self.v5 = int()
		self.v6 = int()
		self.v7 = int()
		self.v8 = int()
		self.v9 = int()
	

	def serialize(self):
		s = b''
		
		# serialize self.v0
		s += struct.pack('?', self.v0)
		
		# serialize self.v1
		s += struct.pack('c', self.v1.encode('ascii'))
		
		# serialize self.v10
		s += struct.pack('f', self.v10)
		
		# serialize self.v11
		s += struct.pack('d', self.v11)
		
		# serialize self.v12
		tmp4 = b''
		tmp4 += struct.pack('I', len(self.v12))
		while len(tmp4) and tmp4[-1] == b'\x00'[0]:
			tmp4 = tmp4[:-1]
		s += struct.pack('B', len(tmp4))
		s += tmp4
		
		s += self.v12.encode('ascii')
		
		# serialize self.v13
		s += struct.pack('b', self.v13.value)
		
		# serialize self.v14
		s += self.v14.serialize()
		
		# serialize self.v15
		tmp5 = b''
		tmp5 += struct.pack('I', len(self.v15))
		while len(tmp5) and tmp5[-1] == b'\x00'[0]:
			tmp5 = tmp5[:-1]
		s += struct.pack('B', len(tmp5))
		s += tmp5
		
		for tmp6 in self.v15:
			s += struct.pack('i', tmp6)
		
		# serialize self.v16
		tmp7 = b''
		tmp7 += struct.pack('I', len(self.v16))
		while len(tmp7) and tmp7[-1] == b'\x00'[0]:
			tmp7 = tmp7[:-1]
		s += struct.pack('B', len(tmp7))
		s += tmp7
		
		for tmp8 in self.v16:
			tmp9 = b''
			tmp9 += struct.pack('I', len(tmp8))
			while len(tmp9) and tmp9[-1] == b'\x00'[0]:
				tmp9 = tmp9[:-1]
			s += struct.pack('B', len(tmp9))
			s += tmp9
			
			for tmp10 in tmp8:
				s += struct.pack('c', tmp10.encode('ascii'))
		
		# serialize self.v17
		tmp11 = b''
		tmp11 += struct.pack('I', len(self.v17))
		while len(tmp11) and tmp11[-1] == b'\x00'[0]:
			tmp11 = tmp11[:-1]
		s += struct.pack('B', len(tmp11))
		s += tmp11
		
		for tmp12 in self.v17:
			tmp13 = b''
			tmp13 += struct.pack('I', len(tmp12))
			while len(tmp13) and tmp13[-1] == b'\x00'[0]:
				tmp13 = tmp13[:-1]
			s += struct.pack('B', len(tmp13))
			s += tmp13
			
			s += tmp12.encode('ascii')
			s += struct.pack('i', self.v17[tmp12])
		
		# serialize self.v18
		tmp14 = b''
		tmp14 += struct.pack('I', len(self.v18))
		while len(tmp14) and tmp14[-1] == b'\x00'[0]:
			tmp14 = tmp14[:-1]
		s += struct.pack('B', len(tmp14))
		s += tmp14
		
		for tmp15 in self.v18:
			s += struct.pack('c', tmp15.encode('ascii'))
			tmp16 = b''
			tmp16 += struct.pack('I', len(self.v18[tmp15]))
			while len(tmp16) and tmp16[-1] == b'\x00'[0]:
				tmp16 = tmp16[:-1]
			s += struct.pack('B', len(tmp16))
			s += tmp16
			
			for tmp17 in self.v18[tmp15]:
				tmp18 = b''
				tmp18 += struct.pack('I', len(tmp17))
				while len(tmp18) and tmp18[-1] == b'\x00'[0]:
					tmp18 = tmp18[:-1]
				s += struct.pack('B', len(tmp18))
				s += tmp18
				
				for tmp19 in tmp17:
					s += struct.pack('d', tmp19)
					s += struct.pack('b', tmp17[tmp19].value)
		
		# serialize self.v19
		for tmp20 in range(10):
			s += struct.pack('b', self.v19[tmp20])
		
		# serialize self.v2
		s += struct.pack('b', self.v2)
		
		# serialize self.v20
		for tmp21 in range(10):
			for tmp22 in range(20):
				tmp23 = b''
				tmp23 += struct.pack('I', len(self.v20[tmp21][tmp22]))
				while len(tmp23) and tmp23[-1] == b'\x00'[0]:
					tmp23 = tmp23[:-1]
				s += struct.pack('B', len(tmp23))
				s += tmp23
				
				for tmp24 in self.v20[tmp21][tmp22]:
					tmp25 = b''
					tmp25 += struct.pack('I', len(tmp24))
					while len(tmp25) and tmp25[-1] == b'\x00'[0]:
						tmp25 = tmp25[:-1]
					s += struct.pack('B', len(tmp25))
					s += tmp25
					
					s += tmp24.encode('ascii')
		
		# serialize self.v3
		s += struct.pack('B', self.v3)
		
		# serialize self.v4
		s += struct.pack('h', self.v4)
		
		# serialize self.v5
		s += struct.pack('H', self.v5)
		
		# serialize self.v6
		s += struct.pack('i', self.v6)
		
		# serialize self.v7
		s += struct.pack('I', self.v7)
		
		# serialize self.v8
		s += struct.pack('q', self.v8)
		
		# serialize self.v9
		s += struct.pack('Q', self.v9)
		
		return s
	

	def deserialize(self, s, offset=0):
		# deserialize self.v0
		self.v0 = struct.unpack('?', s[offset:offset + 1])[0]
		offset += 1
		
		# deserialize self.v1
		self.v1 = struct.unpack('c', s[offset:offset + 1])[0]
		offset += 1
		self.v1 = self.v1.decode('utf-8')
		
		# deserialize self.v10
		self.v10 = struct.unpack('f', s[offset:offset + 4])[0]
		offset += 4
		
		# deserialize self.v11
		self.v11 = struct.unpack('d', s[offset:offset + 8])[0]
		offset += 8
		
		# deserialize self.v12
		tmp26 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		tmp27 = s[offset:offset + tmp26]
		offset += tmp26
		tmp27 += b'\x00' * (4 - tmp26)
		tmp28 = struct.unpack('I', tmp27)[0]
		
		self.v12 = s[offset:offset + tmp28].decode('utf-8')
		offset += tmp28
		
		# deserialize self.v13
		tmp29 = struct.unpack('b', s[offset:offset + 1])[0]
		offset += 1
		self.v13 = EColor(tmp29)
		
		# deserialize self.v14
		if self.v14 is None:
			self.v14 = Child()
		offset = self.v14.deserialize(s, offset)
		
		# deserialize self.v15
		tmp30 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		tmp31 = s[offset:offset + tmp30]
		offset += tmp30
		tmp31 += b'\x00' * (4 - tmp30)
		tmp32 = struct.unpack('I', tmp31)[0]
		
		self.v15 = []
		for tmp33 in range(tmp32):
			tmp34 = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
			self.v15.append(tmp34)
		
		# deserialize self.v16
		tmp35 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		tmp36 = s[offset:offset + tmp35]
		offset += tmp35
		tmp36 += b'\x00' * (4 - tmp35)
		tmp37 = struct.unpack('I', tmp36)[0]
		
		self.v16 = []
		for tmp38 in range(tmp37):
			tmp40 = struct.unpack('B', s[offset:offset + 1])[0]
			offset += 1
			tmp41 = s[offset:offset + tmp40]
			offset += tmp40
			tmp41 += b'\x00' * (4 - tmp40)
			tmp42 = struct.unpack('I', tmp41)[0]
			
			tmp39 = []
			for tmp43 in range(tmp42):
				tmp44 = struct.unpack('c', s[offset:offset + 1])[0]
				offset += 1
				tmp44 = tmp44.decode('utf-8')
				tmp39.append(tmp44)
			self.v16.append(tmp39)
		
		# deserialize self.v17
		tmp45 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		tmp46 = s[offset:offset + tmp45]
		offset += tmp45
		tmp46 += b'\x00' * (4 - tmp45)
		tmp47 = struct.unpack('I', tmp46)[0]
		
		self.v17 = {}
		for tmp48 in range(tmp47):
			tmp51 = struct.unpack('B', s[offset:offset + 1])[0]
			offset += 1
			tmp52 = s[offset:offset + tmp51]
			offset += tmp51
			tmp52 += b'\x00' * (4 - tmp51)
			tmp53 = struct.unpack('I', tmp52)[0]
			
			tmp49 = s[offset:offset + tmp53].decode('utf-8')
			offset += tmp53
			tmp50 = struct.unpack('i', s[offset:offset + 4])[0]
			offset += 4
			self.v17[tmp49] = tmp50
		
		# deserialize self.v18
		tmp54 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		tmp55 = s[offset:offset + tmp54]
		offset += tmp54
		tmp55 += b'\x00' * (4 - tmp54)
		tmp56 = struct.unpack('I', tmp55)[0]
		
		self.v18 = {}
		for tmp57 in range(tmp56):
			tmp58 = struct.unpack('c', s[offset:offset + 1])[0]
			offset += 1
			tmp58 = tmp58.decode('utf-8')
			tmp60 = struct.unpack('B', s[offset:offset + 1])[0]
			offset += 1
			tmp61 = s[offset:offset + tmp60]
			offset += tmp60
			tmp61 += b'\x00' * (4 - tmp60)
			tmp62 = struct.unpack('I', tmp61)[0]
			
			tmp59 = []
			for tmp63 in range(tmp62):
				tmp65 = struct.unpack('B', s[offset:offset + 1])[0]
				offset += 1
				tmp66 = s[offset:offset + tmp65]
				offset += tmp65
				tmp66 += b'\x00' * (4 - tmp65)
				tmp67 = struct.unpack('I', tmp66)[0]
				
				tmp64 = {}
				for tmp68 in range(tmp67):
					tmp69 = struct.unpack('d', s[offset:offset + 8])[0]
					offset += 8
					tmp71 = struct.unpack('b', s[offset:offset + 1])[0]
					offset += 1
					tmp70 = EColor(tmp71)
					tmp64[tmp69] = tmp70
				tmp59.append(tmp64)
			self.v18[tmp58] = tmp59
		
		# deserialize self.v19
		for tmp72 in range(10):
			self.v19[tmp72] = struct.unpack('b', s[offset:offset + 1])[0]
			offset += 1
		
		# deserialize self.v2
		self.v2 = struct.unpack('b', s[offset:offset + 1])[0]
		offset += 1
		
		# deserialize self.v20
		for tmp73 in range(10):
			for tmp74 in range(20):
				tmp75 = struct.unpack('B', s[offset:offset + 1])[0]
				offset += 1
				tmp76 = s[offset:offset + tmp75]
				offset += tmp75
				tmp76 += b'\x00' * (4 - tmp75)
				tmp77 = struct.unpack('I', tmp76)[0]
				
				self.v20[tmp73][tmp74] = []
				for tmp78 in range(tmp77):
					tmp80 = struct.unpack('B', s[offset:offset + 1])[0]
					offset += 1
					tmp81 = s[offset:offset + tmp80]
					offset += tmp80
					tmp81 += b'\x00' * (4 - tmp80)
					tmp82 = struct.unpack('I', tmp81)[0]
					
					tmp79 = s[offset:offset + tmp82].decode('utf-8')
					offset += tmp82
					self.v20[tmp73][tmp74].append(tmp79)
		
		# deserialize self.v3
		self.v3 = struct.unpack('B', s[offset:offset + 1])[0]
		offset += 1
		
		# deserialize self.v4
		self.v4 = struct.unpack('h', s[offset:offset + 2])[0]
		offset += 2
		
		# deserialize self.v5
		self.v5 = struct.unpack('H', s[offset:offset + 2])[0]
		offset += 2
		
		# deserialize self.v6
		self.v6 = struct.unpack('i', s[offset:offset + 4])[0]
		offset += 4
		
		# deserialize self.v7
		self.v7 = struct.unpack('I', s[offset:offset + 4])[0]
		offset += 4
		
		# deserialize self.v8
		self.v8 = struct.unpack('q', s[offset:offset + 8])[0]
		offset += 8
		
		# deserialize self.v9
		self.v9 = struct.unpack('Q', s[offset:offset + 8])[0]
		offset += 8
		
		return offset