using System;
using System.Collections.Generic;

namespace seaBattle
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            var fieldPlayer = new Dictionary<string, char>();
            var fieldEnemy = new Dictionary<string, char>();
            var fieldShow = new Dictionary<string, char>();
            InitField(fieldEnemy);
            InitField(fieldPlayer);
            InitField(fieldShow);

            PlaceShips(fieldPlayer);
            PlaceEnemyShips(fieldEnemy);

            while (true)
            {
                PrintTwoFields(fieldPlayer, fieldShow);
                Attack(fieldEnemy, fieldShow);
                if (CheckWin(fieldEnemy))
                {
                    Console.WriteLine("You WIN!!!!");
                    break;
                }

                AttackEnemy(fieldPlayer, fieldPlayer);
                if (CheckWin(fieldPlayer))
                {
                    Console.WriteLine("You LOSE!!!!");
                    break;
                }
            }
        }

        private static void PlaceEnemyShips(Dictionary<string, char> fieldEnemy)
        {
            var random = new Random();
            for (var i = 0; i < 18; i++)
                PlaceEnemyShip(fieldEnemy, random);
        }

        private static void PlaceEnemyShip(Dictionary<string, char> fieldEnemy, Random random)
        {
            var alf = "abcdefghij";
            var input = alf[random.Next(0, alf.Length)] + random.Next(1, 11).ToString();
            if (fieldEnemy[input] != '@')
                fieldEnemy[input] = '@';
            else
                PlaceEnemyShip(fieldEnemy, random);
        }

        private static void PlaceShips(Dictionary<string, char> fieldPlayer)
        {
            for (var i = 0; i < 18; i++)
            {
                PrintField(fieldPlayer);
                Console.WriteLine("Place 18 ships");

                PlaceShip(fieldPlayer);
            }
        }


        private static bool CheckWin(Dictionary<string, char> field)
        {
            foreach (var key in field.Keys)
                if (field[key] == '@')
                    return false;
            return true;
        }

        private static void AttackEnemy(Dictionary<string, char> field, Dictionary<string, char> fieldShow)
        {
            var random = new Random();
            var alf = "abcdefghij";
            var input = alf[random.Next(0, alf.Length)] + random.Next(1, 11).ToString();
            var isShip = field[input] == '@';
            field[input] = isShip ? 'x' : '*';
            fieldShow[input] = isShip ? 'x' : '*';
        }

        private static void Attack(Dictionary<string, char> field, Dictionary<string, char> fieldShow)
        {
            var input = Console.ReadLine();
            if (field.ContainsKey(input) && (fieldShow[input] == '.' || fieldShow[input] == '@'))
            {
                var isShip = field[input] == '@';
                field[input] = isShip ? 'x' : '*';
                fieldShow[input] = isShip ? 'x' : '*';
            }
            else
            {
                Console.WriteLine("Wrong input");
                Attack(field, fieldShow);
            }
        }

        private static void PlaceShip(Dictionary<string, char> field)
        {
            var input = Console.ReadLine();
            if (field.ContainsKey(input) && field[input] != '@')
                field[input] = '@';
            else
            {
                Console.WriteLine("Wrong input");
                PlaceShip(field);
            }
        }

        private static void InitField(Dictionary<string, char> field)
        {
            var alf = "abcdefghij";
            for (var i = 0; i < alf.Length; i++)
            for (var j = 0; j < 10; j++)
                field[alf[j] + (i + 1).ToString()] = '.';
        }

        private static void PrintField(Dictionary<string, char> field)
        {
            Console.Clear();
            var alf = "abcdefghij";
            Console.WriteLine("  " + alf);
            for (var i = 0; i < alf.Length; i++)
            {
                Console.Write(i + 1);
                Console.Write(i == 9 ? "" : " ");
                for (var j = 0; j < 10; j++)
                    Console.Write(field[alf[j] + (i + 1).ToString()]);
                Console.WriteLine();
            }
        }

        private static void PrintTwoFields(Dictionary<string, char> field1, Dictionary<string, char> field2)
        {
            Console.Clear();
            var alf = "abcdefghij";
            Console.WriteLine("  " + alf + "   " + alf);

            for (var i = 0; i < alf.Length; i++)
            {
                Console.Write(i + 1);
                Console.Write(i == 9 ? "" : " ");
                for (var j = 0; j < 10; j++)
                    Console.Write(field1[alf[j] + (i + 1).ToString()]);
                Console.Write(" " + (i + 1));
                Console.Write(i == 9 ? "" : " ");
                for (var j = 0; j < 10; j++)
                    Console.Write(field2[alf[j] + (i + 1).ToString()]);

                Console.WriteLine();
            }
        }
    }
}