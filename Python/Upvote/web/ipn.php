<?php
/* This example demonstrates how to use the PayCo.re IPN for multiple products.
** This could be used for multiple license types (different durations).
** It utilizes mysqli as it is more easy to understand for
** inexperienced programmers.
*/

//Get default variables
$transactionID		= getPostVariable('tx_id');
$ipnSecret 		= getPostVariable('ipn_secret');
$paymentStatus		= getPostVariable('status');
$invoiceID 		= getPostVariable('invoice_id');
$productID		= getPostVariable('product_id');
$amount 		= getPostVariable('amount');
$currency 		= getPostVariable('currency');
$paymentMethod 		= getPostVariable('payment_method');
$receiverUsername 	= getPostVariable('receiver_username');
$customerEmail 		= getPostVariable('customer_email');

//Get custom form field varialbes
$hwid 				= $_POST['custom_form_fields']['URL'];

//Step 1 - Validate IPN secret & get product details:

$productCurrency 	= "USD";
$sellerUsername		= "furz";

switch ($ipnSecret) {
    case 'productsecret1':
        $licenseDuration = 2592000; //30 days
        $productPrice = 10;
        break;
    case 'productsecret2':
        $licenseDuration = 7776000; //90 days
        $productPrice = 15;
        break;
    case 'productsecret3':
        $licenseDuration = 15552000; //180 days
        $productPrice = 20;
        break;
    case 'productsecret4':
        $licenseDuration = 315569260; //10 years
        $productPrice = 35;
        break;
    default:
        //If no valid secret was provided:
        debugDie('incorrect secret');
        break;
}

//Step 2 - Validate payment status:
if($paymentStatus != "complete") debugDie('payment not completed yet');
//Step 3 - Validate payment amount:
if($amount != $productPrice) debugDie('invalid payment amount');
//Step 4 - Validate payment currency:
if($currency != $productCurrency) debugDie('invalid currency');
//Step 5 - Validate receiver username:
if($receiverUsername != $sellerUsername) debugDie('incorrect receiver');

/* Now you should check if the transaction is already known, so you don't proccess it twice
** This is very unlikely to happen, but you still should do this to avoid conflicting database
** entries */
$mysqli = new mysqli($dbhost, $dbuser, $dbpass, $dbname);
if(mysqli_connect_errno()) debugDie('unable to connect to database');
$tx_id = $mysqli->real_escape_string($tx_id);
$query = "SELECT * FROM paycore_transactions WHERE tx_id = '$tx_id'";
if($result = $mysqli->query($query)){
    if($result->num_rows != 0) debugDie('transaction is already known');
    /* If the transaction isn't known yet you should insert it into the the table that contains the known
    ** transactions, always make sure to escape the strings to avoid SQLi vulnerability */
    $result->close();
    $time = time();
    $invoiceID = $mysqli->real_escape_string($invoiceID);
    $paymentMethod = $mysqli->real_escape_string($paymentMethod);
    $hwid = $mysqli->real_escape_string($hwid);
    $username= $mysqli->real_escape_string($username);
    $query = "INSERT INTO paycore_transactions (tx_id, invoice_id, payment_method, time)
	VALUES('$tx_id', '$invoiceID', '$paymentMethod', '$time')";
    $mysqli->query($query);
    /* After inserting the transaction you can continue to perform any required queries your system needs.
    ** In example inserting some data from custom form fields into an user table in order to provide access
    ** to your product to your customer.
    ** In this example we calculate a timestamp the license expires on and insert the provided details into
    ** a table that holds the licenses */
    $time = time();
    $expiryTime = $time + $licenseDuration;
    $query = "INSERT INTO users VALUES(NULL, '$hwid', '$username', '$expiryTime', NULL, NULL)";
    $mysqli->query($query);
    $mysqli->close();
}else{
    debugDie('database error');
}


function debugDie($sMessage){
    //Your debugging code
    die($sMessage);
}

function getPostVariable($sKey){
    return (isset($_POST[$sKey]) ? $_POST[$sKey] : false);
}