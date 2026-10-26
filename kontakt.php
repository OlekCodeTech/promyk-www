<?php
// Obsługa formularza kontaktowego PROMYK — wysyłka na info@promyk.wielun.pl
// (statyczna strona + PHP na hostingu home.pl)

$TO   = 'info@promyk.wielun.pl';
$FROM = 'formularz@promyk.wielun.pl';
$BACK = 'kontakt';
// reCAPTCHA v3 — wpisz klucz tajny z konta Google klienta (pusty = wyłączona; działa wtedy pułapka + kontrola czasu)
$RECAPTCHA_SECRET = '';

function back($q) {
    global $BACK;
    header('Location: ' . $BACK . '?' . $q . '#formularz', true, 303);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') back('');

// pułapka na boty (ukryte pole) — bot je wypełni, człowiek nie
if (!empty($_POST['www'])) back('wyslano=1');

// formularz wysłany szybciej niż w 3 s od wczytania strony = automat
$ts = isset($_POST['ts']) ? (int)$_POST['ts'] : 0;
if ($ts > 0 && (time() * 1000 - $ts) < 3000) back('blad=1');

if ($RECAPTCHA_SECRET !== '') {
    $resp = @file_get_contents('https://www.google.com/recaptcha/api/siteverify', false, stream_context_create(['http' => [
        'method'  => 'POST',
        'header'  => "Content-Type: application/x-www-form-urlencoded\r\n",
        'content' => http_build_query(['secret' => $RECAPTCHA_SECRET, 'response' => $_POST['g-recaptcha-response'] ?? '', 'remoteip' => $_SERVER['REMOTE_ADDR'] ?? '']),
        'timeout' => 8,
    ]]));
    $r = $resp ? json_decode($resp, true) : null;
    if (!$r || empty($r['success']) || ($r['score'] ?? 0) < 0.5) back('blad=1');
}

$clean = function ($k, $max = 200) {
    $v = isset($_POST[$k]) ? trim((string)$_POST[$k]) : '';
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max, 'UTF-8');
};
$name  = $clean('name', 120);
$tel   = $clean('tel', 40);
$email = $clean('email', 160);
$cat   = $clean('kategoria', 80);
$msg   = isset($_POST['message']) ? mb_substr(trim((string)$_POST['message']), 0, 5000, 'UTF-8') : '';
$zgoda = !empty($_POST['zgoda']);

if ($name === '' || $tel === '' || $msg === '' || !$zgoda || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    back('blad=1');
}
foreach ([$name, $tel, $email, $cat] as $v) {
    if (preg_match('/[\n]/', $v)) back('blad=1');   // ochrona przed wstrzyknięciem nagłówków
}

$subject = 'Zapytanie ze strony: ' . ($cat !== '' ? $cat : 'kontakt') . ' — ' . $name;
$body = "Nowe zapytanie ze strony promyk.wielun.pl\n\n"
      . "Imię i nazwisko: $name\n"
      . "Telefon: $tel\n"
      . "E-mail: $email\n"
      . "Kategoria: $cat\n\n"
      . "Wiadomość:\n$msg\n\n"
      . "---\nZgoda na przetwarzanie danych: TAK\n"
      . 'Data: ' . date('Y-m-d H:i') . "\n"
      . 'IP: ' . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n";

$headers  = 'From: =?UTF-8?B?' . base64_encode('Strona PROMYK') . "?= <$FROM>\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";

$ok = mail($TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $FROM);
back($ok ? 'wyslano=1' : 'blad=1');
