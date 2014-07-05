
	$(document).ready(function() {
		
		var main = '.micropress-main',
			content = '.micropress-post',
			container = '.micropress-container',
			
			isMain = function() {
				if (location.pathname == '/') {
					return true;
				}
				
				return false;
			},
			
			getSelector = function() {
				if (isMain()) {
					return main;
				}
				
				return content;
			},
			
			getContainer = function() {
				var name;
				
				if (isMain()) {
					name = container; 
				} else {
					name = content;
				}
				
				return $(name);
			};
		
		setInterval(function() {
			var selector = getSelector(),
				$container = getContainer();
			
			$container.load(location.href + ' ' + selector, function() {
				var $main, data;
				
				if (isMain()) {
					$main = $(main).first();
					data = $container.find(main).html();
				
					if (data != $main.html()) {
						$main.html(data);
					}
				}
			});
		}, 2000);
		
	});