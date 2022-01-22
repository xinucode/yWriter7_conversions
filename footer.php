<div class="home-link">
	<div class="color-form">
      <a class='navigation' href="../index.php"><img src="../img/Melogo2-backgroundremoved.png" alt="Xinu" class="home-link"></a>
	  <?php if($prev_page !== ""): ?>
	  <a class='navigation' href='<?php echo $prev_page;?>?font=<?php echo $this_font;?>&color_scheme=<?php echo $color_scheme;?>&font_size=<?php echo $font_size;?>&search_type=Change+Settings'><center>&lt Previous Page</center></a>
	  <?php endif; ?>
	  <p class="footer">##this_page_number## of ##total_pages##</p>
	  <?php if($next_page !== ""): ?>
	  <a class='navigation' href='<?php echo $next_page;?>?font=<?php echo $this_font;?>&color_scheme=<?php echo $color_scheme;?>&font_size=<?php echo $font_size;?>&search_type=Change+Settings'><center>Next Page &gt</center></a>
	  <?php endif; ?>
	</div>
</div>

</div>
</body></html>