<?php
    $mysql = mysql_connect('localhost', 'section9', 'section9');
    mysql_select_db('section9');

    $query = 'SELECT id,ip,latitude,longitude FROM geoipdata where complete = 1';
	//echo $query;
    $res = mysql_query($query);

    // iterate over every row
    while ($row = mysql_fetch_assoc($res)) {
        // for every field in the result..
        for ($i=0; $i < mysql_num_fields($res); $i++) {
            $info = mysql_fetch_field($res, $i);
            $type = $info->type;

            // cast for real
            if ($type == 'real')
                $row[$info->name] = doubleval($row[$info->name]);
            // cast for int
            if ($type == 'int')
                $row[$info->name] = intval($row[$info->name]);
        }

        $rows[] = $row;
    }

    // JSON-ify all rows together as one big array
    echo json_encode($rows);
    
    mysql_close($mysql);


?>