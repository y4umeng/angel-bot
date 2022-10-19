from requests_oauthlib import OAuth1Session
import random
import requests
from bs4 import BeautifulSoup

headers = {
    'authority': 'cashedcobrazhousewriter.substack.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://cashedcobrazhousewriter.substack.com/', #link to the substack blog
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'xxx',
}
cookies = {
} # cookies may or may not be necessary for Lambda function. 
# Not neccessary for "manual" tweeting (running function on local device)

params = {
    's': 'r',
}

#list of all articles on the blog at the time.
#compiled from html of the substack page
allArticles = ['https://cashedcobrazhousewriter.substack.com/p/notice-me-take-my-hand-why-are-we', 'https://cashedcobrazhousewriter.substack.com/p/theory-of-covers', 'https://cashedcobrazhousewriter.substack.com/p/you-are-too-beautiful-for-hell-to', 'https://cashedcobrazhousewriter.substack.com/p/notes-towards-the-milady-angelicism', 'https://cashedcobrazhousewriter.substack.com/p/the-most-important-thing-in-the-world', 'https://cashedcobrazhousewriter.substack.com/p/i-see-your-face-its-haunting-me-i', 'https://cashedcobrazhousewriter.substack.com/p/if-we-are-below-that-number-this', 'https://cashedcobrazhousewriter.substack.com/p/notes-21', 'https://cashedcobrazhousewriter.substack.com/p/we-may-soon-never-be-here-again', 'https://cashedcobrazhousewriter.substack.com/p/n-i-k-e-s-angelicism-and-bierasure', 'https://cashedcobrazhousewriter.substack.com/p/notes-on-god-the-vibe-shift-water', 'https://cashedcobrazhousewriter.substack.com/p/somebody-please-columbine-the-entire-e73', 'https://cashedcobrazhousewriter.substack.com/p/8b7', 'https://cashedcobrazhousewriter.substack.com/p/covid-genocide', 'https://cashedcobrazhousewriter.substack.com/p/tell-me-what-angelicism-is-now-or', 'https://cashedcobrazhousewriter.substack.com/p/elemental-poster-profiles-by-mara', 'https://cashedcobrazhousewriter.substack.com/p/why-is-benjamin-brattonbutton-working', 'https://cashedcobrazhousewriter.substack.com/p/i-am-so-scared-of-extinction', 'https://cashedcobrazhousewriter.substack.com/p/dj-slurrr-heaven-or-las-vegas-angelicism01', 'https://cashedcobrazhousewriter.substack.com/p/wet-brain-discord-archive-part-1', 'https://cashedcobrazhousewriter.substack.com/p/dear-thus-come-gone-one', 'https://cashedcobrazhousewriter.substack.com/p/go-anna', 'https://cashedcobrazhousewriter.substack.com/p/color-singularity', 'https://cashedcobrazhousewriter.substack.com/p/dj-slurrr-slurrrgaze-singularity', 'https://cashedcobrazhousewriter.substack.com/p/pure-open-intelligence-rainbow-singularity', 'https://cashedcobrazhousewriter.substack.com/p/sorry-haters-but-hitler-never-had', 'https://cashedcobrazhousewriter.substack.com/p/the-biggest-difference-between-me', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-20', 'https://cashedcobrazhousewriter.substack.com/p/pure-yassified-wow-wow-wow', 'https://cashedcobrazhousewriter.substack.com/p/choreo-pop-techno-regimes-on-kissing', 'https://cashedcobrazhousewriter.substack.com/p/angelicism01-2021-acultural-100', 'https://cashedcobrazhousewriter.substack.com/p/melting-person-6-unidentifiable-poems', 'https://cashedcobrazhousewriter.substack.com/p/4c7', 'https://cashedcobrazhousewriter.substack.com/p/you-deserve-to-die-more-than-me', 'https://cashedcobrazhousewriter.substack.com/p/random-notes-scanner-2021', 'https://cashedcobrazhousewriter.substack.com/p/angelicism-initializing-logic-', 'https://cashedcobrazhousewriter.substack.com/p/2-xmas-autofictions-by-angelicism01', 'https://cashedcobrazhousewriter.substack.com/p/the-all-has-taken-its-toll-masha', 'https://cashedcobrazhousewriter.substack.com/p/go-to-china-when-america-became-china', 'https://cashedcobrazhousewriter.substack.com/p/human-and-ai-mindwar-above-the-mytho-ab1', 'https://cashedcobrazhousewriter.substack.com/p/antigone-as-usual-or-rex-hofman-buried', 'https://cashedcobrazhousewriter.substack.com/p/golden-emptiness-iterated', 'https://cashedcobrazhousewriter.substack.com/p/infinite-redacted-blah-blah-thus', 'https://cashedcobrazhousewriter.substack.com/p/so-vulnerable-2', 'https://cashedcobrazhousewriter.substack.com/p/war-notes-the-angel-war-was-a-soundcloud', 'https://cashedcobrazhousewriter.substack.com/p/impermanence-4', 'https://cashedcobrazhousewriter.substack.com/p/revulsion-and-vulnerability', 'https://cashedcobrazhousewriter.substack.com/p/note-to-reader', 'https://cashedcobrazhousewriter.substack.com/p/adamantine-diginity-1', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-xi', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-19', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-x', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-ix', 'https://cashedcobrazhousewriter.substack.com/p/impermanence-10', 'https://cashedcobrazhousewriter.substack.com/p/impermanence-8-9', 'https://cashedcobrazhousewriter.substack.com/p/2-more-statements-of-identity', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-viii', 'https://cashedcobrazhousewriter.substack.com/p/simple-statements-on-emptiness', 'https://cashedcobrazhousewriter.substack.com/p/convergence-1952', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-18', 'https://cashedcobrazhousewriter.substack.com/p/angelicism01-reviews-donda', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-vii', 'https://cashedcobrazhousewriter.substack.com/p/writing-for-self-extinction', 'https://cashedcobrazhousewriter.substack.com/p/what-is-angelicic-griefing', 'https://cashedcobrazhousewriter.substack.com/p/statement-of-perfect-intelligence', 'https://cashedcobrazhousewriter.substack.com/p/-spot', 'https://cashedcobrazhousewriter.substack.com/p/no-milady-nfts-not-now-the-return', 'https://cashedcobrazhousewriter.substack.com/p/my-hypergraphia-is-exploitable-but', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-vi', 'https://cashedcobrazhousewriter.substack.com/p/statement-of-identity', 'https://cashedcobrazhousewriter.substack.com/p/a-45-hour-episode-on-the-texts-of', 'https://cashedcobrazhousewriter.substack.com/p/angels-and-sex-introduction', 'https://cashedcobrazhousewriter.substack.com/p/to-be-not-pedantic', 'https://cashedcobrazhousewriter.substack.com/p/10-statements-of-identity', 'https://cashedcobrazhousewriter.substack.com/p/the-august-2021-love-poems-by-angelicism01', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-the-vibe-shift-vs-the-discord', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-17', 'https://cashedcobrazhousewriter.substack.com/p/radical-symbiosis-part-2-should-i', 'https://cashedcobrazhousewriter.substack.com/p/e4f', 'https://cashedcobrazhousewriter.substack.com/p/even-so-come-quickly-lord-jesus', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-v', 'https://cashedcobrazhousewriter.substack.com/p/name-the-podcast-challenge', 'https://cashedcobrazhousewriter.substack.com/p/poco-allegra', 'https://cashedcobrazhousewriter.substack.com/p/somebody-please-take-a-gchq-angle', 'https://cashedcobrazhousewriter.substack.com/p/autofiction-5-by-angelicism01', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-jon-rafmans-new-tiktok', 'https://cashedcobrazhousewriter.substack.com/p/antigone-has-two-heads', 'https://cashedcobrazhousewriter.substack.com/p/the-deleted-tweets-poems-a-selection', 'https://cashedcobrazhousewriter.substack.com/p/pocket-angelicisms-or-the-languages', 'https://cashedcobrazhousewriter.substack.com/p/part-iv', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-iii', 'https://cashedcobrazhousewriter.substack.com/p/the-death-of-sophia-vanderbilt-iteration', 'https://cashedcobrazhousewriter.substack.com/p/end-of-universe-part-ii', 'https://cashedcobrazhousewriter.substack.com/p/the-end-of-the-universe-part-i', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-16', 'https://cashedcobrazhousewriter.substack.com/p/the-loving-paths', 'https://cashedcobrazhousewriter.substack.com/p/-the-pure-vibe-poems-read-by-soph', 'https://cashedcobrazhousewriter.substack.com/p/lindy-does-not-exist-a-reply-to-sean', 'https://cashedcobrazhousewriter.substack.com/p/mcdonalds-is-mathematically-impossible', 'https://cashedcobrazhousewriter.substack.com/p/9-random-tweets-from-2020', 'https://cashedcobrazhousewriter.substack.com/p/white-pooh-shiestys-shooting-victim', 'https://cashedcobrazhousewriter.substack.com/p/on-god-the-simone-weil-poems', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-15', 'https://cashedcobrazhousewriter.substack.com/p/alt-lit-is-extinct', 'https://cashedcobrazhousewriter.substack.com/p/antigone-chainsaw-massacre-fragment', 'https://cashedcobrazhousewriter.substack.com/p/2300-gods-bf-jeans-pov', 'https://cashedcobrazhousewriter.substack.com/p/autofiction-4-by-angelicism01', 'https://cashedcobrazhousewriter.substack.com/p/list-of-lists-part-2-e48', 'https://cashedcobrazhousewriter.substack.com/p/what-is-the-internet-according-to', 'https://cashedcobrazhousewriter.substack.com/p/what-is-the-mtv-archive-waiting-for', 'https://cashedcobrazhousewriter.substack.com/p/what-i-dreamt-last-night', 'https://cashedcobrazhousewriter.substack.com/p/i-want-to-die-by-covid', 'https://cashedcobrazhousewriter.substack.com/p/autofiction-3-by-angelicism01', 'https://cashedcobrazhousewriter.substack.com/p/i-have-not-taken-the-vaccine', 'https://cashedcobrazhousewriter.substack.com/p/the-new-york-poems-by-angelicism01', 'https://cashedcobrazhousewriter.substack.com/p/autofiction-02-by-angelicism01', 'https://cashedcobrazhousewriter.substack.com/p/the-internet-has-gone-i-will-carry', 'https://cashedcobrazhousewriter.substack.com/p/the-frustration-economy', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-14', 'https://cashedcobrazhousewriter.substack.com/p/11-tweets-of-early-2021-in-no-particular', 'https://cashedcobrazhousewriter.substack.com/p/radical-symbiosis', 'https://cashedcobrazhousewriter.substack.com/p/subtlety', 'https://cashedcobrazhousewriter.substack.com/p/messiah-of-the-kiss-towards-a-theory', 'https://cashedcobrazhousewriter.substack.com/p/grothendieck-said-stop', 'https://cashedcobrazhousewriter.substack.com/p/sky-flower-mind', 'https://cashedcobrazhousewriter.substack.com/p/portrait-of-giancarlo-ditrapano-as', 'https://cashedcobrazhousewriter.substack.com/p/infinitely-dividing-sunflowers-9b0', 'https://cashedcobrazhousewriter.substack.com/p/covid-has-pinocchio', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-13', 'https://cashedcobrazhousewriter.substack.com/p/random-notes-on-paimon-and-satan', 'https://cashedcobrazhousewriter.substack.com/p/purity', 'https://cashedcobrazhousewriter.substack.com/p/honor-leviticus-90210-excerpt', 'https://cashedcobrazhousewriter.substack.com/p/list-of-lists-part-1', 'https://cashedcobrazhousewriter.substack.com/p/cirular-raibw-monaseris', 'https://cashedcobrazhousewriter.substack.com/p/twitter-memory-2-broken-nfts-missing', 'https://cashedcobrazhousewriter.substack.com/p/two-teenage-girls-by-vincent-gallo', 'https://cashedcobrazhousewriter.substack.com/p/autofiction-1-by-angelicism01-', 'https://cashedcobrazhousewriter.substack.com/p/universal-lyric', 'https://cashedcobrazhousewriter.substack.com/p/circular-rainbow-monasteries', 'https://cashedcobrazhousewriter.substack.com/p/ten-quotes', 'https://cashedcobrazhousewriter.substack.com/p/the-retard-list-ii', 'https://cashedcobrazhousewriter.substack.com/p/soundcloud-infinite-niches-axioms', 'https://cashedcobrazhousewriter.substack.com/p/no-nfts-not-now-the-return-of-post', 'https://cashedcobrazhousewriter.substack.com/p/-nl-', 'https://cashedcobrazhousewriter.substack.com/p/the-more-i-think-about-total-extinction', 'https://cashedcobrazhousewriter.substack.com/p/common-perception', 'https://cashedcobrazhousewriter.substack.com/p/dunton-street-home-for-wayward-girls', 'https://cashedcobrazhousewriter.substack.com/p/lean-when-you-walk', 'https://cashedcobrazhousewriter.substack.com/p/why-wait-for-death', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-quiet-rap', 'https://cashedcobrazhousewriter.substack.com/p/pure-buoyancy', 'https://cashedcobrazhousewriter.substack.com/p/i-only-want-a-rainbow-writing', 'https://cashedcobrazhousewriter.substack.com/p/heidegger-on-nfts', 'https://cashedcobrazhousewriter.substack.com/p/the-skinny-on-spiritual-bouyancy', 'https://cashedcobrazhousewriter.substack.com/p/im-using-a-kathy-acker-chainsaw-to', 'https://cashedcobrazhousewriter.substack.com/p/down-to-rape', 'https://cashedcobrazhousewriter.substack.com/p/rip-dean-kissick', 'https://cashedcobrazhousewriter.substack.com/p/legalise-heroin-fragments', 'https://cashedcobrazhousewriter.substack.com/p/post', 'https://cashedcobrazhousewriter.substack.com/p/rip-kantbot-the-extinct', 'https://cashedcobrazhousewriter.substack.com/p/absolute--intelligence', 'https://cashedcobrazhousewriter.substack.com/p/not-for-want-of-kissing', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-jh-prynne-2019-2021-and', 'https://cashedcobrazhousewriter.substack.com/p/22-posts-using-virgil-ablohs-3-rule', 'https://cashedcobrazhousewriter.substack.com/p/sofia-coppola-century-city-cajanuary', 'https://cashedcobrazhousewriter.substack.com/p/the-retard-list', 'https://cashedcobrazhousewriter.substack.com/p/dasha-crab-walk', 'https://cashedcobrazhousewriter.substack.com/p/i-have-no-idea-whats-going-on', 'https://cashedcobrazhousewriter.substack.com/p/substack-on-tucker-carlson-screenshots', 'https://cashedcobrazhousewriter.substack.com/p/paris-august-whispered-bamboo-sleep', 'https://cashedcobrazhousewriter.substack.com/p/the-stupidity-of-the-most-intelligent', 'https://cashedcobrazhousewriter.substack.com/p/the-first-jacques-derrida-deepfake', 'https://cashedcobrazhousewriter.substack.com/p/on-the-non-fungibility-of-the-human', 'https://cashedcobrazhousewriter.substack.com/p/simple-and-extended-fugue-around', 'https://cashedcobrazhousewriter.substack.com/p/somebody-please-columbine-the-entire', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-dzogchen', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-12', 'https://cashedcobrazhousewriter.substack.com/p/on-the-rewritability-of-finnegans', 'https://cashedcobrazhousewriter.substack.com/p/hey', 'https://cashedcobrazhousewriter.substack.com/p/beauty-and-the-universe', 'https://cashedcobrazhousewriter.substack.com/p/e-girls-and-buddhism', 'https://cashedcobrazhousewriter.substack.com/p/twitter-memory-1-ai-writing-reading', 'https://cashedcobrazhousewriter.substack.com/p/all-good', 'https://cashedcobrazhousewriter.substack.com/p/encore-un-effort-for-ld50-1', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-michelle-carter', 'https://cashedcobrazhousewriter.substack.com/p/nfts-finitude', 'https://cashedcobrazhousewriter.substack.com/p/i-dont-give-a-shit-about-all-life', 'https://cashedcobrazhousewriter.substack.com/p/all-quirked-up-with-nowhere-to-go', 'https://cashedcobrazhousewriter.substack.com/p/lee-kang-shengs-ass', 'https://cashedcobrazhousewriter.substack.com/p/bs-or-bernie-sanders', 'https://cashedcobrazhousewriter.substack.com/p/how-to-read-like-a-quirked-up-shawty', 'https://cashedcobrazhousewriter.substack.com/p/quirked-up-shawties-vs-the-ccp-or', 'https://cashedcobrazhousewriter.substack.com/p/infinitely-dividing-sunflowers', 'https://cashedcobrazhousewriter.substack.com/p/will-they-ever-get-past-arizona-a', 'https://cashedcobrazhousewriter.substack.com/p/the-resurrection-of-ld50-propositions', 'https://cashedcobrazhousewriter.substack.com/p/reaction-harmony-korine-hitler-mitchell', 'https://cashedcobrazhousewriter.substack.com/p/marc-elias-daddy-of-the-legal-hoard', 'https://cashedcobrazhousewriter.substack.com/p/relapse-notes-on-tom-cohens-work', 'https://cashedcobrazhousewriter.substack.com/p/hannah-black-talks-about-the-dalai', 'https://cashedcobrazhousewriter.substack.com/p/what-are-the-rules-of-racism', 'https://cashedcobrazhousewriter.substack.com/p/clueless', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-judith-butlers-voter-fraud', 'https://cashedcobrazhousewriter.substack.com/p/note-on-that-time-when-hannah-black', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-11', 'https://cashedcobrazhousewriter.substack.com/p/butterflymaybe-i-was-hito-steyerl', 'https://cashedcobrazhousewriter.substack.com/p/the-great-invisible-beauty', 'https://cashedcobrazhousewriter.substack.com/p/notes-on-the-china-fetish', 'https://cashedcobrazhousewriter.substack.com/p/google-cancelled-my-email-account', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-all-tomorrows-parties-and', 'https://cashedcobrazhousewriter.substack.com/p/five-mini-theses-on-tibetan-self', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-incitation', 'https://cashedcobrazhousewriter.substack.com/p/random-ripyobu-aphorisms', 'https://cashedcobrazhousewriter.substack.com/p/the-mystical-underground-part-2', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-andrea-long-chu', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-10', 'https://cashedcobrazhousewriter.substack.com/p/a-note-on-the-social-network-2010', 'https://cashedcobrazhousewriter.substack.com/p/the-legal-rights-of-life-in-america', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-9', 'https://cashedcobrazhousewriter.substack.com/p/this-person-does-not-exist', 'https://cashedcobrazhousewriter.substack.com/p/american-pedo', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-8', 'https://cashedcobrazhousewriter.substack.com/p/rip-kantbot-2020-a-review-part-3', 'https://cashedcobrazhousewriter.substack.com/p/poem-please-please-please-know-that', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-7', 'https://cashedcobrazhousewriter.substack.com/p/negarestani-defends-moynihan-2020', 'https://cashedcobrazhousewriter.substack.com/p/fully-automatic-angel-further-deleted', 'https://cashedcobrazhousewriter.substack.com/p/the-face-of-eliza-douglas-part-2', 'https://cashedcobrazhousewriter.substack.com/p/the-face-of-eliza-douglas', 'https://cashedcobrazhousewriter.substack.com/p/a-brief-note-for-readers-and-subscribers', 'https://cashedcobrazhousewriter.substack.com/p/binge-watching-the-queens-gambit', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-6-charlie-trie', 'https://cashedcobrazhousewriter.substack.com/p/the-five-different-types-of-the-end', 'https://cashedcobrazhousewriter.substack.com/p/theses-on-the-political-present', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-5', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-4', 'https://cashedcobrazhousewriter.substack.com/p/you-are-helping-this-great-universe', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-3', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-2', 'https://cashedcobrazhousewriter.substack.com/p/anne-imhofs-falcon', 'https://cashedcobrazhousewriter.substack.com/p/reading-notes-1', 'https://cashedcobrazhousewriter.substack.com/p/endology-ai', 'https://cashedcobrazhousewriter.substack.com/p/the-mystical-underground', 'https://cashedcobrazhousewriter.substack.com/p/love-that-is-discourse', 'https://cashedcobrazhousewriter.substack.com/p/i-movie', 'https://cashedcobrazhousewriter.substack.com/p/a-long-time-ago-in-chop-or-the-prohibition', 'https://cashedcobrazhousewriter.substack.com/p/a-portrait-of-donald-trump']


# parses the text extracted by bs4 for a random valid string to tweet. 
# ignores white space / non-post text (to an extent)
# could be cleaned up, and depends on the typical format of the blog
# one could add image parsing functionality too
def get_tweet(link): 
    response = requests.get(link, params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    text = str(soup.get_text("\n"))
    numContain = text.count("\nComment\n")
    if numContain == 1:
        text = text[:text.index("\nComment\n")]
    elif numContain >= 2:
        text = text[text.index("\nComment\n"):text.rindex("\nComment\n")]
    if text.__contains__("0 subscriptions"):
        text = text[:text.index("0 subscriptions")]
    if text.__contains__("\nShare\n"):
        text = text[text.index("\nShare\n")+6:]
    lines = text.split('\n')
    index = 0
    while index < len(lines):
        x = lines[index]
        while not x or x==" Likes" or x==" Retweets" or x=="Comment" or lines[index][:-1].isdigit():
            lines.remove(x)
            if index < len(lines):
                x = lines[index]
            else:
                break
        if not x.__contains__(" ") and index+2 < len(lines):
            lines[index-1] = lines[index-1] + lines[index] + lines[index+1]
            lines = lines[:index] + lines[index+2:]
            index-=1
        index+=1

    if (len(lines) == 0):
        link = random.choice(allArticles)
        return get_tweet(link)
    random_num = random.randrange(0, len(lines))
    tweet = lines[random_num]

    while len(tweet) < 25 and random_num < len(lines)-1:
        random_num+=1
        tweet = tweet + "\n" + str(lines[random_num])
    while len(tweet) < 250 and random_num < len(lines):
        if random.random()>.5:
            random_num+=1
            tweet = tweet + "\n" + lines[random_num % len(lines)]
        else:
            break
    periodCount = tweet.count(". ")
    if periodCount > 3 and len(tweet) > 280:
        sentences = tweet.split(". ")
        random_num = random.randrange(0, len(sentences)-1)
        tweet = sentences[random_num]
        while len(tweet) < 250 and random_num < len(sentences):
            if random.random()>.5:
                random_num+=1
                tweet = tweet + ". " + sentences[random_num % len(sentences)]
            else:
                break

    if len(tweet) > 279:
        tweet = tweet[:279]
    if tweet.__contains__(". ") and tweet.rindex(". ") > 100:
        tweet = tweet[:tweet.rindex(". ")+1]
    if tweet.__contains__("? ") and tweet.rindex("? ") > 100:
        tweet = tweet[:tweet.rindex("? ")+1]
    if tweet.__contains__("! ") and tweet.rindex("! ") > 100:
        tweet = tweet[:tweet.rindex("! ")+1]
    tweet = tweet.replace("\\", "")
    if len(tweet) < 10:
        link = random.choice(allArticles)
        return get_tweet(link)
    return tweet

# keys from twit dev account
keys = {
    'CONSUMER_API_KEY': 'xxx',
    'CONSUMER_API_SECRET_KEY': 'xxx',
    'ACCESS_TOKEN': 'xxx-xxx',
    'ACCESS_TOKEN_SECRET': 'xxx',
}

#function that AWS lambda communicates with, calling it when it gets the signal
def handler(event, context):
    consumer_key = keys.get('CONSUMER_API_KEY')
    consumer_secret = keys.get('CONSUMER_API_SECRET_KEY')
    link = random.choice(allArticles)
    text = get_tweet(link)
    payload = {"text": text}

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=keys.get('ACCESS_TOKEN'),
        resource_owner_secret=keys.get('ACCESS_TOKEN_SECRET'),
    )
    # Making the request
    oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

#uncomment following line to test tweet functionality. should tweet on your desired account
handler(0,0)