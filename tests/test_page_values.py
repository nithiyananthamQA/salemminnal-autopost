"""tools/make_page.py: this page's own values (a copy of Kovai Minnal with the district's words)"""
import re, subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "research_free"), str(ROOT / "poster")]
import allnews, post, validate      # noqa: E402


class PageValues(unittest.TestCase):
    def test_names(self):
        self.assertEqual(post.PAGE, "salem")
        self.assertEqual(post.TAG, "#SalemMinnal")
        self.assertEqual(validate.LAST, "மேலும் செய்திகளுக்கு சேலம் மின்னல் பக்கத்தை பின்தொடருங்கள்.")
        self.assertEqual(post.FOLLOW_LINE, validate.LAST)

    def test_own_district_only(self):
        self.assertTrue(allnews.has_place("சேலம்யில் பேருந்து விபத்து"))
        self.assertTrue(allnews.other_district("கோவையில் பேருந்து விபத்து"))
        self.assertTrue(allnews.other_district("செங்கல்பட்டு அருகே விபத்து") or "salem" == "chengalpattu")

    def test_area_news_in_state_news_out(self):      # owner 18 Nov: Chennai's real headlines (17 Nov list + its best reels)
        if "salem" != "chennai":
            return
        own = ["சென்னையில் நாளை மிக கனமழை: ஆரஞ்ச் அலர்ட்", "வடபழனியில் பிரியாணி கடையில் தீ விபத்து", "தாம்பரம் அருகே லாரி மோதி இருவர் பலி",
               "சென்னையில் 1,610 தெருவிளக்குகள் எரியவில்லை", "வேளச்சேரியில் குடிநீர் விநியோகம் நிறுத்தம்", "அரும்பாக்கத்தில் பெண்ணுக்கு தொல்லை",
               "எண்ணூரில் பறவை மோதி ஆளில்லா விமானம் நொறுங்கியது", "கொருக்குப்பேட்டையில் போதை மாத்திரை விற்ற மூவர் கைது",
               "திருவான்மியூரில் டிஜிட்டல் மோசடி விழிப்புணர்வு", "அம்பத்தூர் அருகே லாரி மோதி மாணவி பலி", "ஆவடியில் வீட்டில் திருட்டு",
               "கூடுவாஞ்சேரி அருகே தகராறில் ஒருவர் உயிரிழப்பு", "ஓய்வுபெற்றார் தோனி! சென்னை சூப்பர் கிங்ஸ் ஆலோசகராக நியமனம்!",
               "மெட்ரோ ரயில் சேவை நாளை மாற்றம்", "குரோம்பேட்டையில் நாளை மின்தடை"]
        for t in own:
            self.assertTrue(allnews.has_place(t), t)
            self.assertFalse(allnews.outside_district(t), t)
        state = ["“சமூக நீதி என்ற பெயரில் மத அரசியல் செய்கிறதா தவெக அரசு?” - நயினார் நாகேந்திரன்",
                 "மேகேதாட்டு விவகாரத்தில் தமிழக அரசு ஏன் இன்னும் அனைத்துக்கட்சி கூட்டத்தை கூட்டவில்லை",
                 "திருச்செந்தூர் சூரசம்ஹார விவகாரம்: எடப்பாடி பழனிசாமி கண்டனம்", "“ரீல்ஸ் மோகத்தில் அமைச்சர்கள் காவல் நிலையங்களில் ஆய்வு செய்வது தவறு”"]
        for t in state:
            self.assertTrue(allnews.statewide(t) or allnews.outside_district(t), t)
        self.assertTrue(allnews.other_district("செங்கல்பட்டு அருகே விபத்து"))      # the far town stays another district
        self.assertTrue(len(allnews.COIMBATORE_WORDS) > 150)
        import sys as _s
        _s.path.insert(0, str(ROOT / "poster"))
        import freshness as F      # 19 Nov: the same cut from a second paper; the city name alone never makes two cuts one
        a_h, a_s = "சென்னையில் நாளை மின்தடை", "நாளை (நவம்பர் 21) வேளச்சேரி, தரமணி, அடையாறு பகுதிகளில் மின்தடை."
        self.assertTrue(F.same_cut_areas(a_h, a_s, "2026-11-20", "சென்னை: நாளை மின்தடை", "நாளை (நவம்பர் 21) அடையாறு, வேளச்சேரி பகுதிகள்.", "2026-11-20"))
        self.assertFalse(F.same_cut_areas(a_h, a_s, "2026-11-20", "சென்னையில் நாளை மின்தடை", "நாளை (நவம்பர் 21) தாம்பரம், குரோம்பேட்டை பகுதிகளில் மின்தடை.", "2026-11-20"))

    def test_no_kovai_name_left_in_code(self):
        out = subprocess.run(["grep", "-rIlE", "Kovai Minnal|கோவை மின்னல்|kovai_minnal|KovaiMinnal|kovaiminnal", str(ROOT), "--include=*.py",
                              "--include=*.yml", "--include=*.json", "--exclude-dir=fb_posted", "--exclude-dir=.git", "--exclude-dir=tests"],
                             capture_output=True, text=True).stdout.split()
        self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
