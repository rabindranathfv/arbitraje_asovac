// Script para manejar el comportamiento de los formularios 
$(function() {
	// Event handler para agregar nuevas filas de campos al formulario.
	$('.new-list-item').on('input', function() {
		console.log("input");
		let $clone_target = $(this).closest('div.row')
		let $clone = $clone_target.clone()
		let $name_input = $clone_target.find('div.controls').children().first()
		let $email_input = $clone_target.find('div.controls').children().last()
		let $cloned_name_input = $clone.find('div.controls').children().first()
		let $cloned_email_input = $clone.find('div.controls').children().last()
		console.log($name_input);
		console.log($email_input);
		console.log($cloned_name_input);
		console.log($cloned_email_input);

		let name = $cloned_name_input.attr('name')
		console.log(name);
		let n = parseInt(name.split('_')[2]) + 1
		name = 'recipients_name_' + n
		$cloned_name_input.val('')
		$cloned_name_input.attr('name', name)
		$cloned_name_input.attr('id', 'id_' + name)
		name = 'recipients_email_' + n
		$cloned_email_input.val('')
		$cloned_email_input.attr('name', name)
		$cloned_email_input.attr('id', 'id_' + name)

		$clone.appendTo($clone_target.parent())
		$name_input.removeClass('new-list-item')
		$email_input.removeClass('new-list-item')
		$name_input.off('input', arguments.callee)
		$email_input.off('input', arguments.callee)
		$cloned_name_input.on('input', arguments.callee)
		$cloned_email_input.on('input', arguments.callee)
	})

	// Handlers para ocultar filas de campos vacios.
	$(document).on('blur', 'form input[name^=recipients_name_]:not(.new-list-item)', function(){
		let $hide_target = $(this).closest('div.row');
		console.log("BLUR from " + $(this).attr('name'));
		let $email_input = $hide_target.find('div.controls').children().last();
		console.log($hide_target);
		console.log("email")
		console.log($email_input.attr('id'));
		let value1 = $(this).val();
		let value2 = $email_input.val();
		if (value1 === "" && value2 === "" && $email_input.attr('id') != 'id_recipients_email_0') {
			$hide_target.slideUp();
		}
	})

	$(document).on('blur', 'form input[name^=recipients_email_]:not(.new-list-item)', function(){
		let $hide_target = $(this).closest('div.row');
		console.log("BLUR from " + $(this).attr('name'));
		let $name_input = $hide_target.find('div.controls').children().first();
		console.log($hide_target);
		console.log("nombre")
		console.log($name_input.attr('id'));
		let value1 = $(this).val();
		let value2 = $name_input.val();
		if (value1 === "" && value2 === "" && $name_input.attr('id') != 'id_recipients_name_0') {
			$hide_target.slideUp();
		}
	})
});