<?php 
?>
<!DOCTYPE html>
<html>
<head>
	<title>logIn</title>
</head>
<script type="text/javascript">
	addr="<?php echo $_SERVER['SERVER_ADDR'];?>";
	if(addr=="::1")
		addr="localhost";
	localStorage.setItem("addr",addr);
	console.log(addr);
	function check_domain()
	{	email=document.getElementById("email").value.toLowerCase();
		splitted_email=email.split("@");
		//console.log(splitted_email[1]);
		if(splitted_email[1]!="mailit.com")
		{	//css
			alert("wrong domain");
			return false;
		}
		return true;
	}
	function send_form(){
		if(check_domain())
		{ 	
			var email=document.getElementById("email").value.toLowerCase();
			var password=document.getElementById("password").value;
			var xhr=new XMLHttpRequest();

			var url="http://"+addr+":1000/login";
			;
			// console.log(document.getElementById("email").value);
			// console.log(document.getElementById("password").value)
			var params="email="+email+"&password="+password;
			
			xhr.open('POST',url,true);
			console.log("here")
			xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
			//storing the state information of the user.

			localStorage.setItem("email",email);
			xhr.onreadystatechange = function() {
			    if(this.readyState == 4){
					if(this.status == 200) {

			        	window.location.assign("home.php");
			        	// document.writeln("success");
			    	}
			    	else if(this.status==400)
			    	{	
			    		alert("incorrect email or password");
			    	}
			     	else
			    	{
			    		console.log("some error");
			    	}
				}
			}
			
			xhr.send(params);
			console.log("sent");
		}	
	}
</script>
<body>
	<form>
		<label>Email</label><input type="email" name="email" id="email" onblur="check_domain()" required><br/>
		<label>Password</label><input type="password" name="password" id="password" required><br/>
		<input type="button" value="submit" onclick="send_form()"><br/>
		<a href="create_account.php">create account</a>
	</form>
</body>

</html> 