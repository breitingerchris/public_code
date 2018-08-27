<?php
function mt_rand_str ($l, $c = 'abcdefghijklmnopqrstuvwxyz1234567890') {
    for ($s = '', $cl = strlen($c)-1, $i = 0; $i < $l; $s .= $c[mt_rand(0, $cl)], ++$i);
    return $s;
}
$profit = number_format(0.00000000, 8);
$turnsBefore = 0;
$totalTurns = 0;
$origbet =  0.000005;
$over = false;
$overCount = 0;
$lower = 0;
$bet = number_format($origbet, 8);
while (1)
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://win88.me/dice/play');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Cookie: __RequestVerificationToken=AQyPJt1OUMUute2F7n-hEkAB0; _ga=GA1.2.1593279570.1410469765; btc-pid=KiQLaUb3OPmMLs3GARS2amkdnAcMpWSrsGmnXA9AQFXvSpMLZ8oyMwaf7ufazQO174bFFQtARRlXRxN8yTyqqdf5nHpkchK90ex; __atuvc=3%7C37; _cb_ls=1; _chartbeat2=C-bPzvxAOFCDVFpbD.1410469769729.1410482074195.1; _chartbeat_uuniq=3; btc-googid=u9URzFW0SV7FZ6RfY5N8q5KTiBsRbpwgY8pE2lneKq5_yJGaOlbnsFbyhY-2AG-SI5yxFIUN1kZuJ4d-TopevHBtm85nw5FA_nSmKtqj9mypcbUKzZZ7_FjCUBgGx8q_SslddbA3Tl0m2L0EVpddxxZqDNnktHZFWsH_NBM7jCHPx0EfAxHbrH5a2EPPjennefUv1Nshxn_XSwOQ9h-6mFUlT42ptD9YOeOkI4vRP4b; lastNewsId=23; _we_wk_ss_lsf_=true; __zlcmid=Qme3EBe1kZI9Zj; betAmount=%220.00000000%22; betsTabIndex=1; chatVisible=1; playMpSound=1; playChatSound=false; _gat=1',
        'Accept: application/json, text/plain, */*',
        'Content-Type: application/json'
    ));
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0');
    curl_setopt($ch, CURLOPT_REFERER, 'https://win88.me/');
    curl_setopt($ch, CURLOPT_POST, 1);
    $payload = array(
        'BetAmount' => $bet,
        'ClientSeed' => mt_rand_str(12),
        'Over' => $over,
        'WinChance' => '90.5000',
        'Edge' => '99'
    );
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    $result = curl_exec($ch);
    curl_close($ch);
    $errorsucces = json_decode($result, true);
    if ($errorsucces['AlertType'] == 'danger')
    {
        $turnsBefore = 0;
        $overCount = 0;
        $lower = 0;
        $profit -= number_format($errorsucces['AlertParam2'], 8);
    } else {
        $turnsBefore++;
        $overCount++;
        $lower++;
        $profit += number_format($errorsucces['AlertParam2'], 8) - $bet;
    }
    if ($overCount >= 3)
    {
        $overCount = 0;
        $over = !$over;
    }
    if ($bet != $origbet)
    {
        $bet = $origbet;
    }
    if ($lower == 3)
    {
        $bet = number_format(0.0001, 8);
    } elseif ($lower >= 6) {
        $bet = number_format(0.0000035, 8);
    }elseif ($lower == 10) {
        $bet = number_format(0.0001, 8);
    } elseif ($lower >= 15){
        $bet = number_format(0.00000035, 8);
    }
    $totalTurns++;
    echo "\n" . "\n" . "\n" . "\n" . "\n" . "\n";
    echo  'Current Bet: ' . $bet . "\n";
    echo  'Winning Streak: ' . $turnsBefore . "\n";
    echo  'Total Bets: ' . $totalTurns . "\n";
    echo  'Profit: ' . number_format($profit, 8) . "\n";
    sleep(0.75);
}