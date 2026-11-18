<?php

/** Generates a deterministic error through the application's normal logging path. */
class XSentryProbeAction extends CAction
{
    /** @var string|null Secret supplied by deployment configuration; empty disables the action. */
    public $token;
    /** @var string|null Optional operator-only test label, never read from a request. */
    public $marker;

    public function run()
    {
        if(!is_string($this->token) || $this->token==='')
            throw new CHttpException(404, 'The requested page does not exist.');

        // Keep the secret out of URLs, Yii's REQUEST_URI log and Sentry request extras.
        $authorization=isset($_SERVER['HTTP_AUTHORIZATION']) ? $_SERVER['HTTP_AUTHORIZATION'] : null;
        if(!is_string($authorization)
            || preg_match('/\ABearer ([^\s]+)\z/i', $authorization, $matches)!==1
            || !hash_equals($this->token, $matches[1]))
            throw new CHttpException(403, 'You are not allowed to access this page.');

        // Yii's error handler supplies the error-level log and HTTP 500 response.
        // The configured XSentryLogRoute retains its normal grouping and throttling.
        $message='Kaardid Sentry probe';
        if(is_string($this->marker) && preg_match('/\A[A-Z][A-Z0-9_-]{0,79}\z/D',$this->marker))
            $message.=' ['.$this->marker.']';
        throw new CHttpException(500, $message);
    }
}
