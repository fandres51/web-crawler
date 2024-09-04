from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .views import fetch_news_entries, filter_entries, count_words

class NewsCrawlerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('news_entries')

    @patch('api.views.fetch_news_entries')
    def test_news_entries_view(self, mock_fetch_news_entries):
        # Mock data returned by fetch_news_entries
        mock_fetch_news_entries.return_value = [
            {
                'number': 1,
                'title': 'This is a long title with more than five words',
                'points': 150,
                'comments': 60
            },
            {
                'number': 2,
                'title': 'Short title',
                'points': 200,
                'comments': 10
            }
        ]

        # Send GET request to the news endpoint
        response = self.client.get(self.url)

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check the structure of the returned data
        response_data = response.json()
        self.assertIn('long_titles_sorted', response_data)
        self.assertIn('short_titles_sorted', response_data)

        # Check if the data is sorted correctly
        self.assertEqual(len(response_data['long_titles_sorted']), 1)
        self.assertEqual(len(response_data['short_titles_sorted']), 1)

        self.assertEqual(response_data['long_titles_sorted'][0]['title'], 'This is a long title with more than five words')
        self.assertEqual(response_data['short_titles_sorted'][0]['title'], 'Short title')

    def test_filter_entries(self):
        entries = [
            {
                'number': 1,
                'title': 'This is a long title with more than five words',
                'points': 150,
                'comments': 60
            },
            {
                'number': 2,
                'title': 'Short title',
                'points': 200,
                'comments': 10
            },
            {
                'number': 3,
                'title': 'Another long title with even more words in it',
                'points': 300,
                'comments': 90
            },
            {
                'number': 4,
                'title': 'Tiny',
                'points': 50,
                'comments': 5
            }
        ]

        long_titles_sorted, short_titles_sorted = filter_entries(entries)

        # Check that the long titles are sorted by comments
        self.assertEqual(long_titles_sorted[0]['number'], 3)
        self.assertEqual(long_titles_sorted[1]['number'], 1)

        # Check that the short titles are sorted by points
        self.assertEqual(short_titles_sorted[0]['number'], 2)
        self.assertEqual(short_titles_sorted[1]['number'], 4)

    @patch('api.views.requests.get')
    def test_fetch_news_entries(self, mock_get):
        # Mock the HTML response from the news website
        mock_html = '''
        <html>
            <body>
                <tr class="athing" id="1">
                    <span class="rank">1.</span>
                    <span class="titleline">
                        <a class="storylink">This is a long title with more than five words</a>
                    </span>
                </tr>
                <tr>
                    <td class="subtext">
                        <span class="score">150 points</span>
                        <a href="item?id=1">60 comments</a>
                    </td>
                </tr>
                <tr class="athing" id="2">
                    <span class="rank">2.</span>
                    <span class="titleline">
                        <a class="storylink">Short title</a>
                    </span>
                </tr>
                <tr>
                    <td class="subtext">
                        <span class="score">200 points</span>
                        <a href="item?id=2">10 comments</a>
                    </td>
                </tr>
            </body>
        </html>
        '''

        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_html

        entries = fetch_news_entries()

        # Check the number of entries
        self.assertEqual(len(entries), 2)

        # Check if the entries are correctly parsed
        self.assertEqual(entries[0]['title'], 'This is a long title with more than five words')
        self.assertEqual(entries[0]['points'], 150)
        self.assertEqual(entries[0]['comments'], 60)

        self.assertEqual(entries[1]['title'], 'Short title')
        self.assertEqual(entries[1]['points'], 200)
        self.assertEqual(entries[1]['comments'], 10)
