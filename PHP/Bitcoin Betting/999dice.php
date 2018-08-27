<?php
function mt_rand_str ($l, $c = 'abcdefghijklmnopqrstuvwxyz1234567890')
{
    for ($s = '', $cl = strlen($c)-1, $i = 0; $i < $l; $s .= $c[mt_rand(0, $cl)], ++$i);
    return $s;
}

function sendBet($bet, $target, $session) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://www.999dice.com/api/web.aspx');
    curl_setopt($ch, CURLOPT_PROXY, '127.0.0.1:8888');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, 'a=PlaceBet&s=' . $session['SessionCookie'] . '&PayIn=' . $bet . '&Low=1&High=' . $target . '&ClientSeed=-1445515027485303300&Currency=btc');
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    $result = curl_exec($ch);
    return $result;
}

function martingale($session) {
    $profit = 0;
    $turnsBefore = 0;
    $totalTurns = 0;
    $origbet = 2;
    $bet = $origbet;
    $origtarget = 499499;
    $target = $origtarget;
    $loss = 0;
    $lossBets = 0;
    $i = 0;
    while ($i <= 15000)
    {
        $errorsucces = json_decode(sendBet($bet, number_format($target, $decimals = 0, $dec_point = "", $thousands_sep = ""), $session), true);
        if (isset($errorsucces['PayOut']))
        {
            if (intval($errorsucces['PayOut']) != 0)
            {
                $turnsBefore = 0;
                $profit -= $bet;
                $bet = $origbet;
                $target = $origtarget;
                $loss = 0;
                $lossBets = 0;
            } else {
                $turnsBefore++;
                $loss++;
                $lossBets++;
                $profit += $errorsucces['PayOut'] - $bet;
                if ($loss == 1) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 3) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 7) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 15) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 31) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 63) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 127) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 255) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 511) {
                    $bet *= 2;
                    $target /= 1.75;
                } elseif ($loss == 1023) {
                    $bet *= 2;
                    $target /= 1.75;
                }
            }
        }
        $totalTurns++;
        echo "\n" . "\n" . "\n" . "\n" . "\n" . "\n";
        echo  'Current Bet Value: ' . $bet . "\n";
        echo  'Winning Streak: ' . $turnsBefore . "\n";
        echo  'Total Bets: ' . $totalTurns . "\n";
        echo  'Lost Bets In a Row: ' . $lossBets . "\n";
        echo  'Profit: ' . $profit . "\n";
        sleep(0.25);
        $i++;
    }
}

function startSession ($API, $user, $pass)
{
    if (file_exists('login.json'))
    {
        return json_decode(file_get_contents('login.json'), true);
    } else {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://www.999dice.com/api/web.aspx');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, 'a=Login&Key=' . $API . '&Username=' . $user . '&Password=' . $pass);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        $result = curl_exec($ch);
        curl_close($ch);
        file_put_contents('login.json', $result);
        return json_decode($result, true);
    }
}

$API = '61f556f4c6be408f92bb4687f354b0ed';
$User = 'thewhitewox';
$Pass = 'playtime2';
$session = startSession($API, $User, $Pass);
martingale($session);