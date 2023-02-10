from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

	def __init__(self,color='Cyan'):

		self.depth  = 3
		
		self.string1 = f'<material name="{color}">'

		if color=='Cyan':
			self.string2 = f'    <color rgba="0 1.0 1.0 1.0"/>'
		else:
			self.string2 = f'    <color rgba="0 {float(color=="Green")} {float(color=="Blue")} 1.0"/>'

		self.string3 = '</material>'

	def Save(self,f):

		Save_Whitespace(self.depth,f)

		f.write( self.string1 + '\n' )

		Save_Whitespace(self.depth,f)

		f.write( self.string2 + '\n' )

		Save_Whitespace(self.depth,f)

		f.write( self.string3 + '\n' )
