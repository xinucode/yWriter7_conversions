<?php 
// include '..//db.php'; 
error_reporting(E_ERROR | E_PARSE);

try{
$color_scheme = $_GET["color_scheme"];
}
catch(Exception $e){
$color_scheme = "wrong";
}
// echo $color_scheme;
if( $color_scheme == "wb" ){
	$background_color = "black";
	$font_color = "white";
}
else if( $color_scheme == "gb" ){
	$background_color = "black";
	$font_color = "#049604"; //green
}
else if( $color_scheme == "gy" ){
	$background_color = "#FFF9D1"; //yellow
	$font_color = "#049604";
}
else{
	$color_scheme = "bw";
	$background_color = "white";
	$font_color = "black";
}

try{
$font_size = $_GET["font_size"];
$font_size = trim($font_size);
$font_size = stripslashes($font_size);
$font_size = htmlspecialchars($font_size);
}
catch(Exception $e){
$font_size = 5;
}

if (!is_numeric($font_size)){
	$font_size = 5;
}
else if($font_size<2) {
	$font_size = 2;
}
else if ($font_size>15) {
	$font_size = 15;
}


try{
$this_font = $_GET["font"];
}
catch(Exception $e){
$this_font = "times";
}
if( $this_font != "dyslexie" ){
	$this_font = "times";
}

try{
	$b_line = $_GET["bline"];
	if($b_line !== "true"){
		$b_line = False;
	}
}
catch(Exception $e){
$b_line = False;
}

$prev_page = "##prev_page##";
$this_page = "##this_page##";
$next_page = "##next_page##";

if( $prev_page!=="" ){ 
	$prev_page.="?font={$this_font}&color_scheme={$color_scheme}&font_size={$font_size}"; 
	if($b_line){
		$prev_page.="&bline=true";
	}
	$prev_page.="&search_type=Change+Settings";
}
if( $next_page!=="" ){ 
	$next_page.="?font={$this_font}&color_scheme={$color_scheme}&font_size={$font_size}"; 
	if($b_line){
		$next_page.="&bline=true";
	}
	$next_page.="&search_type=Change+Settings";
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>##title##</title>                                          <!-- Templatemo style -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300,400">        <!-- Google web font "Open Sans" -->
  <link rel="stylesheet" href="../css/bootstrap.min.css">                                            <!-- https://getbootstrap.com/ -->
  <link rel="stylesheet" href="../css/fontawesome-all.min.css">
  <link rel="icon" href="../MeLogo3-purple-circle2.png">
  <script>
    var renderPage = true;

    if (navigator.userAgent.indexOf('MSIE') !== -1
      || navigator.appVersion.indexOf('Trident/') > 0) {
      /* Microsoft Internet Explorer detected in. */
      alert("Please view this in a modern browser such as Chrome or Microsoft Edge.");
      renderPage = false;
    }
  </script>
  
  <style type=text/css>

	html, body, div{ padding: 20px; background-color: <?php echo $background_color;?>;}, h1, h2, h3, h4, h5, h6, ul, ol, dl, li, dt, dd, p, blockquote, pre, form, fieldset, table, th, td, tr { margin: 0em; padding: 0.1em; }

	img.home-link {
		max-height: 70px;
		height: 100%;
	}
	@font-face {
		font-family: OpenDyslexic;
		src: url("open_dyslexic/OpenDyslexic-Regular.otf") format("regular");
		src: url("open_dyslexic/OpenDyslexic-Italic.otf") format("italics");
	}
	div.home-link {
		display: flex;
		flex-direction: row;
		// background-color: blue;
		padding: 0px;
		justify-content: center;
		align-items: center;
		width: 100%;
	}
	div.cover-image {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
		// background-color: blue;
		float: right;
		// width: 50%;
	}
	img.cover-image {
		max-width: 400px;
		width: 100%;
		height: auto;
		margin-left: auto;
		margin-right: auto;
		display: flex;
		align: center;
		border: 10px solid <?php echo (substr($color_scheme,1,1)=='b') ? "#049604" : "black"; ?>;
    }
	div.final-image {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column;
		// background-color: blue;
		// float: right;
		// width: 50%;
	}
    div.color-form {
		color: yellow;
		background-color: #7a8528;
		border: 10px solid #343523;
		display: flex;
		flex-direction: row;
		justify-content: space-evenly;
		align-items: center;
		width: 100%;
	}
	div.color-form2 {
		color: yellow;
		background-color: #7a8528;
		display: flex;
		flex-direction: row;
		padding: 0px;
		white-space: nowrap;
		justify-content: flex-start;
		flex-wrap: wrap;
	}
	div.color-form3 {
		color: yellow;
		background-color: #7a8528;
		display: flex;
		flex-direction: column;
		padding: 5px;
	}
	p
	{
		text-indent: 1.2em;
		color: <?php echo $font_color;?>;
		font-family: Arial, Helvetica, sans-serif;
	}
	p.Para{
		<?php if($this_font=="times"):?>font-family: "Times New Roman", Times, serif;<?php endif;?>
		
		<?php if($this_font=="dyslexie"):?>font-family: OpenDyslexic;<?php endif;?>
		line-height: <?php echo ($font_size*8.0);?>px;
		<?php if($b_line):?>
		background-color: black;
		<?php if($color_scheme=="gb"||$color_scheme=="gy"):?>
		background-image: url('text_green_yellow.png');
		<?php elseif($color_scheme=="bw"):?>
		background-image: url('dark_black_blue_red.png');
		<?php else:?>
		background-image: url('light_white_blue_red.png');
		<?php endif;?>
		background-repeat: repeat-y;
		background-size: 100% <?php echo ($font_size*8.0*5.0);?>px;
		background-clip: text;
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		<?php endif;?>
	}
	p.title
	{
		font-size: 1.5em;
		// font-weight: bold;
		margin-top: 2em;
		text-align: center;
	}

	p.headline
	{
		text-align: center;
		text-indent: 0.2em;
		font-weight: bold;
		margin-top: 0.5em;
	}

	p.chapter
	{
		text-indent: 0.2em;
		page-break-before: always;
		// font-weight: bold;
		font-size: 1.5em;
		text-align: center;
		margin-top:0em;
		margin-bottom:0em;
	}
    h1.title {
		// font-weight: bold;
		font-size: 4em;
		text-align: center;
		margin-top:1em;
		margin-bottom:0em;
		color: <?php echo $font_color;?>;
	}
	h2.title {
		// font-weight: bold;
		text-align: center;
		color: <?php echo $font_color;?>;
		margin-top:1em;
	}
	p.centered
	{
		text-indent: 0.2em;
		text-align: center;
	}
	
	span.centered
	{
		text-indent: 0.2em;
		text-align: center;
	} 
	a.navigation {
		color: yellow;
		align: center;
	}
	a.paralink{
		text-decoration: none;
	}
	p.footer{
		color: orange;
		align: center;
	}
	.noselect {
	-webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
	}

</style>

</head>

<body>
<div class="home-link">
	<div class="color-form">
	  <a class='navigation' href="../index.php"><img src="../img/Melogo2-backgroundremoved.png" alt="Xinu" class="home-link"></a>
	  <?php if($prev_page !== ""): ?>
	  <a class='navigation' href='<?php echo $prev_page;?>'><center>&lt Previous Page</center></a>
	  <?php endif; ?>
	  <form action="<?php echo $this_page;?>" method="GET">
	    <div class="color-form2">
			<div class="color-form3">
				<div class="color-form2"><input type="radio" name="color_scheme" value="bw" <?php if($color_scheme=="bw") echo "checked";?>>Black Text, White Screen</div>
				<div class="color-form2"><input type="radio" name="color_scheme" value="wb" <?php if($color_scheme=="wb") echo "checked";?>>White Text, Black Screen</div>
			<!--</div>
			<div class="color-form3">-->
				<div class="color-form2"><input type="radio" name="color_scheme" value="gb" <?php if($color_scheme=="gb") echo "checked";?>>Green Text, Black Screen</div>
				<div class="color-form2"><input type="radio" name="color_scheme" value="gy" <?php if($color_scheme=="gy") echo "checked";?>>Green Text, Yellow Screen</div>
			</div>
			<div class="color-form3">
				<div class="color-form2"><input type="radio" name="font" value="times" <?php if($this_font=="times") echo "checked";?>>Times New Roman</div>
				<div class="color-form2"><input type="radio" name="font" value="dyslexie" <?php if($this_font=="dyslexie") echo "checked";?>>Dyslexie</div>
				<div class="color-form2"><input type="checkbox" name="bline" value="true" <?php if($b_line) echo "checked";?>>Varying Colors</div>
			</div>
			<div class="color-form3">
				<input type="text" name="font_size" class="form-control" placeholder="Type font size number..." value=<?php echo $font_size;?>>
			<!--</div>
			<div class="color-form3">-->
				<input type="submit" name="search_type" value="Change Settings" class="form-control tm-search-submit">
			</div>
		</div>
	  </form>
	  <?php if($next_page !== ""): ?>
	  <a class='navigation' href='<?php echo $next_page;?>'><center>Next Page &gt</center></a>
	  <?php endif; ?>
    </div>
</div>
<h1 class="title"><b>##title##</b></h1>
<h2 class="title"><b>##title##</b></h2>
<div class="noselect">
<font name='arial' size="<?php echo $font_size;?>px">

<p class='chapter'><b>Chapter 1</b></p>
<div class="cover-image">
  
  <img src="##image##" alt="##title##" class="cover-image">
</div>