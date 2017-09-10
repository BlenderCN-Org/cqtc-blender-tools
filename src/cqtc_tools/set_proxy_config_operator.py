import bpy.ops
import bpy.types

class SetProxyConfigOperator(bpy.types.Operator):
	bl_idname = "cqtc_tools_proxy.set_proxy"
	bl_label = "Aplicar configuración Proxy"
	
	def execute(self, context):
		proxyable_sequences = [seq for seq in context.selected_sequences if "proxy" in dir(seq)]
		error = self.__validate(context, proxyable_sequences)
		if error:
			(error_result, error_msg) = error
			self.report(error_result, error_msg)
			return {"CANCELLED"}
		
		for sequence in proxyable_sequences:
			sequence.use_proxy = True
			sequence.proxy.quality = context.scene.cqtc_tools_proxy.jpeg_quality
			sequence.proxy.build_25 = True
		
		if context.scene.cqtc_tools_proxy.rebuild:
			bpy.ops.sequencer.rebuild_proxy()
		
		self.report({"INFO"}, "%i strips reconstruidas" % len(proxyable_sequences) )
		
		return {"FINISHED"}
	
	
	def __validate(self, context, proxyable_sequences):
		if len(context.selected_sequences) == 0:
			return ({"ERROR"}, "No hay strips seleccionadas" )
		
		if len(proxyable_sequences) == 0:
			return ({"ERROR"}, "No se puede aplicar el proxy a ninguna de las strips seleccionadas" )
	