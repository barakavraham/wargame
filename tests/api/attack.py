import json
from app import db
from app.models.army import BattleResult, Army, Upgrade
from app.models.user import User
from tests.api import APITestCase
from tests.utils import format_response


class AttackAPITestCase(APITestCase):
    def tearDown(self):
        self.logout()
        BattleResult.query.delete()
        Upgrade.query.delete()
        Army.query.delete()
        User.query.delete()

    def test_profile_window(self):
        url = '/api/attack/user_profile'
        current_user = self.create_user(email='attacker@test.com', password='111111', army_name='my_user')
        self.login(email='attacker@test.com', password='111111')
        other_user = self.create_user(email='attacked@test.com', password='111111', army_name='other_user')
        res = self.test_client.get(f'{url}/{current_user.id}', follow_redirects=True)
        self.assertIn(f'<h3 class="text-white">{current_user.army.name}</h3>', res.json)
        res = self.test_client.get(f'{url}/{other_user.id}', follow_redirects=True)
        self.assertIn('<a class="mt-3" id="attack-btn"', res.json)

    def test_attack(self):
        url = '/api/attack/attack'
        attacker = self.create_user(email='attacker@test.com', password='111111', army_name='attacker')
        attacked = self.create_user(email='attacked@test.com', password='111111', army_name='attacked')
        self.login(email='attacker@test.com', password='111111')
        attacker.army.turns = 0
        db.session.commit()
        res = self.test_client.post(url, data={
            'attacker_user_id': attacker.id,
            'attacked_user_id': attacked.id,
            'weapon_types': json.dumps('')
        })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message'], 'Invalid weapon types')

        res = self.test_client.post(url, data={
            'attacker_user_id': attacker.id,
            'attacked_user_id': attacked.id,
            'weapon_types': json.dumps(['ground_weapons'])
        })
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['message'], 'You do not have enough turns to attack')

        attacker.army.turns = 100
        db.session.commit()
        res = self.test_client.post(url, data={
            'attacker_user_id': attacker.id,
            'attacked_user_id': attacked.id,
            'weapon_types': json.dumps(['ground_weapons', 'air_weapons'])
        })
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json['url'])
        res = self.test_client.get(res.json['url'], follow_redirects=True)
        self.assertIn('alt="Rifles" /> 0</p>', res.data.decode())
        attacker.army.tank = 300
        attacked.army.tank = 400
        db.session.commit()
        res = self.test_client.post(url, data={
            'attacker_user_id': attacker.id,
            'attacked_user_id': attacked.id,
            'weapon_types': json.dumps(['ground_weapons'])
        })
        battle_result_id = int(res.json['url'].split('/')[-1])
        battle_result = BattleResult.query.get(battle_result_id)
        lost_tanks = battle_result.attacker_result['tank']
        res = self.test_client.get(res.json['url'], follow_redirects=True)
        self.assertIn(f'alt="Tanks" /> {lost_tanks}</p>', res.data.decode())
