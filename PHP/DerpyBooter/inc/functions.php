<?php
class user
{
    function LoggedIn()
    {
        @session_start();
        if (isset($_SESSION['username'], $_SESSION['ID']))
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}

class ParallelGet
{
    function __construct($urls)
    {
        $mh = curl_multi_init();
        foreach($urls as $i => $url)
        {
            $ch[$i] = curl_init($url);
            curl_setopt($ch[$i], CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch[$i], CURLOPT_NOBODY, TRUE);
            curl_multi_add_handle($mh, $ch[$i]);
        }
        do {
        $execReturnValue = curl_multi_exec($mh, $runningHandles);
        } while ($execReturnValue == CURLM_CALL_MULTI_PERFORM);
        while ($runningHandles && $execReturnValue == CURLM_OK) {
            $numberReady = curl_multi_select($mh);
            if ($numberReady != -1) {
                do {
                $execReturnValue = curl_multi_exec($mh, $runningHandles);
                } while ($execReturnValue == CURLM_CALL_MULTI_PERFORM);
            }
        }
    }
}
?>
