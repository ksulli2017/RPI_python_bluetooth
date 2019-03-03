
<html>
  <head>
    <title> Player Health Summary</title>
  </head>
  <body>
    <?php 
      $refresh_rate = 5;
      $refresh=sprintf("refresh: %d;", $refresh_rate);
      header($refresh);

      $filename = "/var/www/html/tmp/playerlist.txt";
      clearstatcache(TRUE, $filename);
        
      $fsize=filesize($filename);
      if($filesize === 0)
      {
        return 1;
      }
      $data = file_get_contents($filename);
      $lines =  preg_split("/[\n]/", $data);//tok = strtok($data, "\n");
      //printf("<p> array is %d lines long</p>\r\n", sizeof($lines));
      //printf("<p>Refresh rate = %d, tok = %s, data = %s</p>",$refresh_rate, $tok, $data); 

      printf("<ol>", $tok);
      for($i = 0; $i < sizeof($lines); $i++){
      #for($i = 0; $i < sizeof($lines) - 1; $i++){
        $tok1 = strtok($lines[$i], ",");
        $tok2 = strtok(",");
        $tok3 = strtok(",");
        if($tok1 !== "")
        {
          printf("<li>Player: %s, Heartrate = %s, Bodytemp = %s</li>\r\n", $tok1, $tok2, $tok3);
          $tok = strtok(",");
        }
      }
      printf("</ol>", $token);
    ?>
      
  </body>
</html>
