favourite:function() {
	$("#favourite").click(function() {
		var aid = ${{video.id}}.val();
		$.post("collect_video/", {
			aid : aid
		}, function(response){
			if(response.data=="0"{
				alert("Server Busy!");
				} else {
					alert("Collected Successfully!");
				}, "json");
		})
	})
}
