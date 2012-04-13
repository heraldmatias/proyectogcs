function confirmar(mensaje){
	if (confirm(mensaje))
		return true;
	return false;
}

function provincias(){
        var id= $("#id_region").val();
	var provincia = $("#id_provincia");
	provincia.find('option').remove();
	provincia.append("<option value='' selected>---------</option>");
	$.getJSON('/ubigeo/provincia/json/?r='+id, function(data){
	$.each(data, function(key,value){		
		provincia.append("<option value='"+value.fields.numpro+"'>"+value.fields.provincia+"</option>");
	});
	});
}
