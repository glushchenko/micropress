
	$(document).ready(function() {
		
		var main = '.micropress-main',
			content = '.micropress-post',
			container = '.micropress-container',
			
			isMain = function() {
				if (
					location.pathname == '/' 
					|| location.pathname.indexOf("blog/page") > -1
				) {
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
			},
		
			updater = setInterval(function() {
				var selector = getSelector(),
					$container = getContainer();
				
				if (location.host != '127.0.0.1:8080') {
					clearInterval(updater);
					return false;
				} 
				
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
			}, 1000);
		
	});