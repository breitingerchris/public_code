<?php

function sendBet ($amount, $target, $condition = '<') {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_PROXY, '127.0.0.1:8888');
    curl_setopt($ch, CURLOPT_URL, 'https://api.primedice.com/api/bet?access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTU3NjAsInRva2VuIjoiOTk2NWRjYWJmOTJmNzc4NWM0ZWIzNjFmYWU2YzZmOWIifQ.ZqHNEOjtQNgsONM5t8VLQ4XFbgkr1zWf6aEuFPEbcUo');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2188.2 Safari/537.36');
    curl_setopt($ch, CURLOPT_REFERER, 'https://primedice.com/play');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, 'amount=' . $amount . '&condition=' . $condition . '&target=' . $target);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}

function noneHigh(){
    $profit = 0;
    $totalTurns = 0;
    $toBet = 256159;
    $bet = 0;
    $target = 40;
    $loss = 0;
    $flip = mt_rand(6, 9);
    while (1)
    {
        $betResult = json_decode(sendBet($bet, $target), true);
        if ($betResult['bet']['win'])
        {
            $bet = 0;
            $loss = 0;
            $profit += $betResult['bet']['profit'];
        } else {
            $loss++;
            $profit += $betResult['bet']['profit'];
            $bet = 0;
            if ($loss == $flip) {
                $bet = $toBet;
                $totalTurns++;
                $flip = mt_rand(7, 10);
            }
        }
        $balance = $betResult['user']['balance'];
        echo "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n";
        echo  'Current Bet: ' . $bet . "\n";
        echo  'Total Bets: ' . $totalTurns . "\n";
        echo  'Lost Bets In a Row: ' . $loss . "\n";
        echo  'Target Losses: ' . $flip . "\n";
        echo  'Profit: ' . $profit . "\n";
        echo  'Balance: ' . $balance . "\n";
        usleep(350000);
    }
}

function martingale() {
    $profit = 0;
    $totalTurns = 0;
    $origbet =  250;
    $bet = $origbet;
    $origtarget = 49.50;
    $target = $origtarget;
    $loss = 0;
    $lossBets = 0;
    while (1)
    {
        $betResult = json_decode(sendBet($bet, $target), true);
        if ($betResult['bet']['win'])
        {
            $bet = $origbet;
            $target = $origtarget;
            $loss = 0;
            $lossBets = 0;
            $profit += $betResult['bet']['profit'];
        } else {
            $loss++;
            $lossBets++;
            $profit += $betResult['bet']['profit'];
            if ($loss == 1) {
                $bet *= 2;
                $target /= 2;
            } elseif ($loss == 3) {
                $bet *= 2;
                $target /= 2;
            } elseif ($loss == 7) {
                $bet *= 2;
                $target /= 2;
            } elseif ($loss == 15) {
                $bet *= 2;
                $target /= 2;
            } elseif ($loss == 31) {
                $bet *= 2;
                $target /= 2;
            }
        }
        $balance = $betResult['user']['balance'];
        $totalTurns++;
        echo "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n";
        echo  'Current Bet Value: ' . $bet . "\n";
        echo  'Total Bets: ' . $totalTurns . "\n";
        echo  'Lost Bets In a Row: ' . $lossBets . "\n";
        echo  'Target: ' . $target . "\n";
        echo  'Profit: ' . $profit . "\n";
        echo  'Balance: ' . $balance . "\n";
        usleep(350000);
    }
}

function twentyfour() {
	$profit = 0;
    $totalTurns = 0;
    $origbet =  25;
    $bet = $origbet;
    $origtarget = 24.75;
    $target = $origtarget;
    $lossBets = 0;
    while (1)
    {
        $betResult = json_decode(sendBet($bet, $target), true);
        if ($betResult['bet']['win'])
        {
            $bet = $origbet;
            $target = $origtarget;
            $lossBets = 0;
            $profit += $betResult['bet']['profit'];
        } else {
            $lossBets++;
            $profit += $betResult['bet']['profit'];
			$bet *= 1.25;
        }
        $balance = $betResult['user']['balance'];
        $totalTurns++;
        echo "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n";
        echo  'Current Bet Value: ' . $bet . "\n";
        echo  'Total Bets: ' . $totalTurns . "\n";
        echo  'Lost Bets In a Row: ' . $lossBets . "\n";
        echo  'Target: ' . $target . "\n";
        echo  'Profit: ' . $profit . "\n";
        echo  'Balance: ' . $balance . "\n";
        usleep(350000);
    }
}

function ninetytwo() {
	$profit = 0;
    $totalTurns = 0;
    $origbet =  500000;
    $bet = $origbet;
    $origtarget = 92.00;
    $target = $origtarget;
	$won = 0;
    $lossBets = 0;
	$condition = '%3C';
	$flip = rand(7, 12);
    while (1)
    {
        $betResult = json_decode(sendBet($bet, $target, $condition), true);
        if ($betResult['bet']['win'])
        {
            $bet = $origbet;
            $lossBets = 0;
            $profit += $betResult['bet']['profit'];
			$won++;
			if ($won % $flip == 0) {
				if ($condition == '%3C') {
					$condition = '%3E';
					$target = 8.00;
					$flip = rand(7, 12);
				} elseif ($condition == '%3E') {
					$condition = '%3C';
					$target = 92.00;
					$flip = rand(7, 12);
				}
			}
        } else {
            $lossBets++;
            $profit += $betResult['bet']['profit'];
        }
        $balance = $betResult['user']['balance'];
        $totalTurns++;
        echo "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n" . "\n";
        echo  'Current Bet Value: ' . $bet . "\n";
        echo  'Total Bets: ' . $totalTurns . "\n";
        echo  'Lost Bets In a Row: ' . $lossBets . "\n";
        echo  'Target: ' . $target . "\n";
        echo  'Profit: ' . $profit . "\n";
        echo  'Balance: ' . $balance . "\n";
        usleep(350000);
    }
}

function thrifyfive() {
	$profit = 0;
    $totalTurns = 0;
    $origbet =  1;
    $bet = $origbet;
    $origtarget = 35.42;
    $target = $origtarget;
	$won = 0;
    $lossBets = 0;
    while (1)
    {
        $betResult = json_decode(sendBet($bet, $target), true);
        if ($betResult['bet']['win'])
        {
            $lossBets = 0;
            $profit += $betResult['bet']['profit'];
			$won++;
        } else {
            $lossBets++;
            $profit += $betResult['bet']['profit'];
        }
        $balance = $betResult['user']['balance'];
        $totalTurns++;
        echo "\n" . "\n" . "\n" . "\n" . "\n" . "\n";
        echo  'Current Bet Value: ' . $bet . "\n";
        echo  'Total Bets: ' . $totalTurns . "\n";
        echo  'Lost Bets In a Row: ' . $lossBets . "\n";
        echo  'Target: ' . $target . "\n";
        echo  'Profit: ' . $profit . "\n";
        echo  'Balance: ' . $balance . "\n";
        usleep(350000);
    }
}

ninetytwo();