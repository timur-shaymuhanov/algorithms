#include <iostream>
#include <vector>
#include <cstring>
#include <random>

using namespace std;

struct User
{
    int score;
    string name;

    User(string n, int sc)
    {
        name = n;
        score = sc;
    }

    int GetScore() const
    {
        return score;
    }

    string GetName() const
    {
        return name;
    }
};

ostream &operator<<(ostream &out, const User &user)
{
    string user_name = user.GetName();
    if (user.GetScore() < 10){
        out << user_name << ": " << string(10 - user_name.length() + 2, ' ') << user.GetScore();
    }
    else{
        out << user_name << ": " << string(10 - user_name.length() + 3 - log10(user.GetScore()), ' ') << user.GetScore();
    }
    return out;
}

void quick_sort(vector<User> &a, int first, int last)
{

    int i = first, j = last;
    User x = a[(first + last) / 2];

    do
    {
        while (a[i].GetScore() < x.GetScore())
            i++;
        while (a[j].GetScore() > x.GetScore())
            j--;

        if (i <= j)
        {
            if (i < j)
            {
                User tmp = a[i];
                a[i] = a[j];
                a[j] = tmp;
            }
            i++;
            j--;
        }
    } while (i <= j);

    if (i < last)
        quick_sort(a, i, last);
    if (first < j)
        quick_sort(a, first, j);
}

vector<User> countable_sort(vector<User> data, int num_of_levels)
{
    vector<User> freq[num_of_levels];
    vector<User> sorted_data;

    for (User user : data)
    {
        freq[user.GetScore()].push_back(user);
    }

    for (vector<User> vec : freq)
    {
        for (User user : vec)
        {
            sorted_data.push_back(user);
        }
    }
    return sorted_data;
};

int main()
{

    vector<string> names = {"Ibrahim", "Peter", "Fatima", "Aleksandr", "Richard", "Xin", "Bin", "Paul", "Ping", "Lin", "Olga", "Sri", "Pedro", "William", "Rosa",
                             "Thomas", "Jorge", "Yong", "Elizabeth", "Sergey", "Ram", "Hassan", "Anita", "Manuel", "Victor", "Sandra", "Ming", "Siti", "Miguel",
                             "Emmanuel", "Samuel", "Ling", "Charles", "Sarah", "Mario", "Joao", "Tatyana", "Mark", "Rita", "Martin", "Svetlana"};

    int score1, score2;
    vector<User> countable_data;
    vector<User> quick_data;

    random_device rd;                          // non-deterministic generator
    mt19937 gen(rd());                         // to seed mersenne twister.
    uniform_int_distribution<> dist1(0, 9);    // distribute results between 0 and 9 inclusive.
    uniform_int_distribution<> dist2(0, 1000); // distribute results between 0 and 9 inclusive.

    for (int i = 0; i < names.size(); i++)
    {
        
        score1 = dist1(gen);
        User user1(names[i], score1);
        countable_data.push_back(user1);

        if (i == 0 || i == 1){
            score2 = 239;
        }
        else{
            score2 = dist2(gen);    
        }
        User user2(names[i], score2);
        quick_data.push_back(user2);
    }

    vector<User> countable_sorted_data = countable_sort(countable_data, 10);
    vector<User> quick_data_copy = quick_data;
    quick_sort(quick_data, 0, quick_data.size() - 1);

    cout << "task1: quick sort" << endl;
    cout << endl;

    cout << "Input:            |   Output:" << "\n";
    cout << "_____________________________________" << "\n";
    cout << "\n";

    for (int i = 0; i < names.size(); i++)
    {
        cout << quick_data_copy[i] << "   |   " << quick_data[i] << endl;
    }

    cout << "task2: countable sort" << endl;
    cout << endl;

    cout << "Input:            |   Output:" << "\n";
    cout << "_____________________________________" << "\n";
    cout << "\n";

    for (int i = 0; i < names.size(); i++)
    {
        cout << countable_data[i] << "   |   " << countable_sorted_data[i] << endl;
    }

}