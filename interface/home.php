<!DOCTYPE html>
<html>
<head>
	<title>mailIt</title>
</head>
<script type="text/javascript">
	// addr="<?php echo $_SERVER['SERVER_ADDR'];?>";
	// if(addr=="::1")
	// 	add="localhost"
	// console.log(addr);
	addr=localStorage.getItem("addr");
	function obj()
	{
		xhr=new XMLHttpRequest();
		this.getData=function()
		{	//user state information is stored in localStorage
			var email=localStorage.getItem("email");
			
			xhr.open('GET','http://'+addr+':1000/getData/'+email,true);
			xhr.onreadystatechange=function()
			{
				if(this.readyState==4)
				{
					if(this.status==200)
					{
						var data=JSON.parse(this.responseText);
						console.log(data[0]['send_email']);
					}
					else
					{
						alert("Failed to load data ~x~");
					}
				}
			}
			xhr.send();
		}
		this.check_email=function(i){
			var email=i.value.toLowerCase();
			splitted_email=email.split("@");
			if(splitted_email[1]!="mailit.com")
			{	//css
				alert("wrong domain");
			}
			else
			{
				var xhr=new XMLHttpRequest();
				var url="http://"+addr+":1000/signup?email="+email;
				xhr.open('GET',url,true);
				xhr.onreadystatechange = function() {
				    if(xhr.readyState == 4){
						if(xhr.status == 200) {
							alert("email does not exists");
				    	}
				    	else if(xhr.status==400)
				    	{	//css
				    		console.log("email exists");
				    	}
				    	else
				    	{	//css
				    		console.log("some error");
				    	}
					}
				}
				xhr.send();
			}

		}
		this.send_email=function()
		{
			xhr.open("POST","http://"+addr+":1000/compose_send",true);
			xhr.setRequestHeader("Content-Type","application/json;charset=UTF-8");
			xhr.onreadystatechange=function()
			{
				if(this.readyState==4 && this.status==200)
				{
					console.log("message delivered");
				}
				else
				{
					console.log("message failed to be delivered");
				}
			};
			data={
				"send_email":localStorage.getItem("email"),
				"recv_email":document.getElementById("recv_email").value,"subject":document.getElementById("subject").value,"body":document.getElementById("body").value
			};

			xhr.send(JSON.stringify(data));
		}

	}
	loader=new obj();
</script>
<body onload="loader.getData()">
	<table id="mailMatrix">
	</table>
	<ifram id="hframe" name="hframe" style="display:hidden;width:0px;height: 0px"></ifram>
	<div>
		<form  target="hframe" id="compose_form">
			<input name="send_email" type="hidden">
			<input type="email" name="recv_email" id="recv_email" placeholder="To" onblur="loader.check_email(this)"><br/>
			<input type="text" name="subject" id="subject" placeholder="Subject"><br/>
			<textarea width="100px" height="100px" name="body" id="body"></textarea><br/>
			<input type="button" value="SEND" onclick="loader.send_email()">
		</form>
	</div>
	
</body>
</html>