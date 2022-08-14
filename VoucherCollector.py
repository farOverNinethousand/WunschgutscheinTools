import argparse
from json import loads


class VoucherCollector:

    def __init__(self, cfg: dict):
        my_parser = argparse.ArgumentParser()
        my_parser.add_argument('-s', '--seconds_between_display_vouchers',
                               help='Wartezeit in Sekunden zwischen Abarbeitung von Einlöselinks.', type=int,
                               default=10)
        my_parser.add_argument('-s2', '--skip_expired_links',
                               help='Abgelaufene Einlöselinks überspringen? False = bei abgelaufenen Links automatische neue zuschicken lassen und die abgelaufenen als abgearbeitet markieren.',
                               type=bool,
                               default=True)
        args = my_parser.parse_args()
        self.skipExpiredLinks = cfg.get('skip_expired_links', args.skip_expired_links)
        self.secondsBetweenDisplayVouchers = int(cfg.get('seconds_between_display_vouchers', args.seconds_between_display_vouchers))
        # self.secondsMaxWaitUntilGiveupOnNoNewRedeemMails = int(cfg.get('seconds_max_wait_until_give_up_on_no_new_redeem_mails', 10))
        self.imap_server = cfg['imap_server']
        self.imap_login = cfg['imap_login']
        self.imap_password = cfg['imap_password']

    def main(self):
        pass

    if __name__ == '__main__':
        pass
