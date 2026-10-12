"""Static customer privacy/identity guards; no fake backend authentication tests."""
import json
from pathlib import Path
import re
import unittest
from seo_audit import Page, ACCOUNT_PAGES, audit
import test_seo_audit as fixtures

ROOT = Path(__file__).resolve().parents[1]
EMAIL = '<input type="email" required autocomplete="username">'
PASSWORD = '<input type="password" required autocomplete="current-password">'
LOGIN = fixtures.GOOD.replace('</main>', '<form method="dialog">'+EMAIL+PASSWORD+'</form></main>')
RECOVERY = fixtures.GOOD.replace('</main>', '<form method="dialog"><input type="email" required autocomplete="email"></form></main>')
CODE = '<input id="code" data-system-code-input type="text" inputmode="numeric" autocomplete="off">'

class AccountTests(unittest.TestCase):
    def errors(self, raw, name='account-orders.html'):
        report = fixtures.AuditGuardTests().check_fixture(raw, page_name=name)
        return '\n'.join(e for p in report['pages'] for e in p['errors'])

    def test_all_eight_pages_participate_in_unweakened_audit(self):
        self.assertEqual(len(ACCOUNT_PAGES), 8)
        self.assertFalse((ROOT/'prototype/account.html').exists())
        self.assertEqual(audit(ROOT)['errors'], 0)
        for name in ACCOUNT_PAGES:
            page = Page(ROOT/'prototype'/name)
            self.assertEqual(page.h1, 1)
            self.assertEqual(page.meta['robots'], 'noindex, nofollow, noarchive')
            self.assertFalse(page.jsonld)
            self.assertFalse(page.canonical)
            self.assertNotIn('brand-intro', page.raw)

    def test_login_uses_mandatory_email_and_current_password(self):
        self.assertEqual(self.errors(LOGIN,'account-login.html'), '')
        self.assertIn('mandatory Email', self.errors(LOGIN.replace('required autocomplete="username"','autocomplete="username"'),'account-login.html'))
        self.assertIn('independent LOGIN', self.errors(LOGIN.replace('</form>','<input name="LOGIN"></form>'),'account-login.html'))
        self.assertIn('autocomplete', self.errors(LOGIN.replace('current-password','new-password'),'account-login.html'))

    def test_registration_has_one_email_and_two_new_passwords(self):
        page = Page(ROOT/'prototype/account-register.html')
        inputs = [a for t,a in page.elements if t=='input']
        self.assertEqual(len([a for a in inputs if a.get('type')=='email']),1)
        passwords = [a for a in inputs if a.get('type')=='password']
        self.assertEqual(len(passwords),2)
        self.assertTrue(all(a['autocomplete']=='new-password' and 'required' in a for a in passwords))
        self.assertFalse(any('required' in a for a in inputs if a.get('type')=='tel' or a.get('id')=='register-name'))
        self.assertFalse(any('minlength' in a or 'pattern' in a for a in passwords))

    def test_recovery_has_only_email_identity(self):
        self.assertEqual(self.errors(RECOVERY,'account-forgot-password.html'),'')
        for field in ('<input type="tel">','<input name="LOGIN">','<input name="system_id">'):
            self.assertIn('only for Email',self.errors(RECOVERY.replace('</form>',field+'</form>'),'account-forgot-password.html'))

    def test_no_structured_data_on_private_account_pages(self):
        for kind in ('Product','Offer','AggregateOffer','Article','Review','AggregateRating','CollectionPage','WebPage'):
            script='<script type="application/ld+json">'+json.dumps({'@type':kind})+'</script>'
            self.assertIn('must not contain structured data',self.errors(fixtures.GOOD.replace('</head>',script+'</head>')))

    def test_metadata_noindex_and_canonical_privacy(self):
        self.assertIn('robots must',self.errors(fixtures.GOOD.replace('noindex, nofollow, noarchive','index, follow')))
        for text in ('customer@review.invalid','KS-2610-0012','DEMO-4102','USER_ID 52002'):
            self.assertIn('metadata must stay generic',self.errors(fixtures.GOOD.replace('<title>Fixture</title>',f'<title>{text}</title>')))
        self.assertIn('canonical',self.errors(fixtures.GOOD.replace('</head>','<link rel="canonical" href="https://review.invalid/account/"> </head>')))

    def test_default_credentials_and_private_fields_are_rejected(self):
        for type in ('password','email','tel','text'):
            raw=fixtures.GOOD.replace('</main>',f'<input type="{type}" value="PRIVATE"></main>')
            self.assertIn('must not prefill',self.errors(raw))
        self.assertIn('hidden identity',self.errors(fixtures.GOOD.replace('</main>','<input type="hidden" name="user_id"></main>')))
        for payload in ('<!-- AUTH_TOKEN=PRIVATE -->', '<script type="application/json">{"SESSION_ID":"PRIVATE"}</script>', '<script type="application/json">{"password":"PRIVATE"}</script>'):
            self.assertIn('token/session payloads', self.errors(fixtures.GOOD.replace('</main>',payload+'</main>')))
        self.assertIn('email-address fixtures', self.errors(LOGIN.replace('</main>', '<p>private@review.invalid</p></main>'), 'account-login.html'))

    def test_customer_system_and_order_cannot_leak_admin_or_secret_data(self):
        fragments=('<!-- SECRET_CODE=1234-5678 -->','<p>1234-5678</p>','<script type="application/json">{"OLD_USER_ID":1}</script>',
                   '<div hidden data-ownership-history>notes</div>','<p>S/N: PRIVATE</p>','<p>DEMO-SN-01</p>',
                   '<input name="SYSTEM_INTERNAL_ID">','<p>SECRET_VERIFIED=true</p>','<p>DEMO-STAFF-A</p>',
                   '<p>SUPPLIER / RMA / SERVICE_HISTORY</p>')
        for name in ('account-systems.html','account-order.html','account-inquiries.html'):
            for fragment in fragments:
                with self.subTest(name=name,fragment=fragment):
                    self.assertIn('private System',self.errors(fixtures.GOOD.replace('</main>',fragment+'</main>'),name))

    def test_code_input_is_only_empty_add_system_field(self):
        raw=fixtures.GOOD.replace('</main>',CODE+'</main>')
        self.assertEqual(self.errors(raw,'account-systems.html'),'')
        self.assertIn('single Add System',self.errors(raw))
        self.assertIn('single Add System',self.errors(raw.replace('</main>',CODE+'</main>'),'account-systems.html'))
        self.assertIn('must not prefill',self.errors(raw.replace('id="code"','id="code" value="1234-5678"'),'account-systems.html'))
        page=Page(ROOT/'prototype/account-systems.html')
        codes=[a for t,a in page.elements if 'data-system-code-input' in a]
        self.assertEqual(len(codes),1)
        self.assertEqual(codes[0]['id'],'add-system-code')
        self.assertNotIn('value',codes[0])

    def test_forms_and_scripts_do_not_authenticate_or_persist(self):
        script=(ROOT/'prototype/assets/js/account.js').read_text()
        self.assertNotRegex(script,r'\b(?:localStorage|sessionStorage|fetch|XMLHttpRequest|randomUUID|randomBytes)\b|Math\.random|crypto\.|document\.cookie|console\.')
        self.assertIn('event.preventDefault()',script)
        for name in ACCOUNT_PAGES:
            for tag,a in Page(ROOT/'prototype'/name).elements:
                if tag=='form':self.assertEqual(a.get('method'),'dialog');self.assertFalse(a.get('action'))
                if tag=='button':self.assertEqual(a.get('type'),'button')
        self.assertIn('non-submitting',self.errors(fixtures.GOOD.replace('</main>','<form method="get" action="account-orders.html"></form></main>')))

    def test_current_account_fixture_does_not_infer_historical_order_access(self):
        fixture=json.loads((ROOT/'docs/frontend/review/account-fixture-v1.json').read_text())
        system=json.loads((ROOT/'docs/frontend/review/system-passport-fixture.json').read_text())
        self.assertEqual(fixture['account_user_id'],system['internal_ownership_review']['system_user_id'])
        self.assertNotEqual(fixture['account_user_id'],system['internal_ownership_review']['initial_order_user_id'])
        for key in ('completed_order','current_order'):self.assertEqual(fixture[key]['user_id'],fixture['account_user_id'])
        self.assertIsNone(fixture['current_order']['systems_user_id'])
        self.assertNotIn(fixture['system_id'],fixture['current_order']['system_ids'])
        self.assertEqual(sum(x['quantity']*x['unit_minor'] for x in fixture['current_order']['items']),fixture['current_order']['total_minor'])
        self.assertNotIn('secret_code',json.dumps(fixture).lower())

    def test_unlink_names_exact_system_and_preserves_confirmed_public_context(self):
        page=Page(ROOT/'prototype/account-systems.html');text=' '.join(page.raw.split())
        self.assertIn('Вы уверены, что хотите отвязать систему KS-2610-0012 от своего аккаунта?',text)
        self.assertIn('Публичный паспорт, гарантия и история компьютера сохранятся.',text)
        self.assertIn('passport.html',page.links)
        self.assertIn('passport.html#inquiry-fallback',page.links)
        self.assertIn('data-pending-ownership',page.raw)
        self.assertNotIn('data-pending-ownership',(ROOT/'prototype/account-inquiries.html').read_text())

    def test_private_routes_are_not_public_footer_or_primary_navigation(self):
        private={'account-orders.html','account-order.html','account-systems.html','account-inquiries.html','account-profile.html'}
        for path in (ROOT/'prototype').glob('*.html'):
            raw=path.read_text()
            for footer in re.findall(r'<footer\b[^>]*>.*?</footer>',raw,re.S):
                for link in private:self.assertNotIn(link,footer,path.name)
            for primary in re.findall(r'<nav\b[^>]*class="k-site-nav"[^>]*>.*?</nav>',raw,re.S):
                self.assertEqual(len(re.findall(r'<a\b',primary)),5,path.name)
                self.assertNotIn('account-',primary,path.name)
        self.assertIn('href="account-login.html"',(ROOT/'prototype/index.html').read_text())
        self.assertFalse(list((ROOT/'prototype').glob('sitemap*')))

    def test_profile_and_private_navigation_contract(self):
        for name in ('account-orders.html','account-order.html','account-systems.html','account-inquiries.html','account-profile.html'):
            page=Page(ROOT/'prototype'/name)
            self.assertIn('data-account-logout',page.raw)
            self.assertEqual(len([a for t,a in page.elements if t=='a' and a.get('aria-current')=='page']),1)
        page=Page(ROOT/'prototype/account-profile.html')
        passwords=[a for t,a in page.elements if t=='input' and a.get('type')=='password']
        self.assertEqual([a['autocomplete'] for a in passwords],['current-password','new-password','new-password'])
        self.assertTrue(all(not a.get('value') and 'minlength' not in a for a in passwords))

if __name__=='__main__':unittest.main()
