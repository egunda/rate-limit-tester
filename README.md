# rate-limit-tester
To test rate limit of any WAF

To execute, use python3 rate-limit-tester.py, enter the target URL and number of threads you want to use. The default thread is set to 10.

# Warnings:

Do not use this tool on a live site!

It is because this tool is designed to perform all kinds of form submissions automatically which can sabotage the site. Sometimes you may screw up the database and most probably perform a DoS on the site as well.

Test on a disposable/dummy setup/site!

# Disclaimer:
Usage of XSRFProbe for testing websites without prior mutual consistency can be considered as an illegal activity. It is the final user's responsibility to obey all applicable local, state and federal laws. The author assumes no liability and is not exclusively responsible for any misuse or damage caused by this program.
