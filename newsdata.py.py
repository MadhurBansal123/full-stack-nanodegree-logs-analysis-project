#!/usr/bin/env python3

import psycopg2

database_nm = "news"

# 1. Which are the three most popular articles of all time?
sol_1 = ("select articles.title, count(*) as views "
    "from articles inner join log on log.path "
    "like concat('%', articles.slug, '%') "
    "where log.status like '%200%' group by "
    "articles.title, log.path order by views desc limit 3")

# 2. Who are the most popular article authors of all time?
sol_2 = (
    "select authors.name, count(*) as views from articles inner "
    "join authors on articles.author = authors.id inner join log "
    "on log.path like concat('%', articles.slug, '%') where "
    "log.status like '%200%' group "
    "by authors.name order by views desc")

# 3. On which days did more than 1% of requests lead to an error?
sol_3 = (
    "select day, perc from ("
    "select day, round((sum(requests)/(select count(*) from log where "
    "substring(cast(log.time as text), 0, 11) = day) * 100), 2) as "
    "perc from (select substring(cast(log.time as text), 0, 11) as day, "
    "count(*) as requests from log where status like '%404%' group by day)"
    "as log_percentage group by day order by perc desc) as final_query "
    "where perc >= 1")


# Storing the results
sol_1_result = dict()
sol_1_result['title'] = "\n1. The 3 most popular articles of all time are:\n"

sol_2_result = dict()
sol_2_result['title'] = """\n2. The most popular article authors of all time are:\n"""

sol_3_result = dict()
sol_3_result['title'] = """\n3. Days with more than 1% of request that lead to an error:\n"""


# this function returns results of queries
def sol_result(query):
    db = psycopg2.connect(database=database_nm)
    data = db.cursor()
    data.execute(query)
    results = data.fetchall()
    db.close()
    return results


def print_results(query_result):
        print(query_result['title'])
        for result in query_result['results']:
            print('\t' + str(result[0]) + ' -----> ' + str(result[1]) + ' views')


def print_error_results(query_result):
    print(query_result['title'])
    for result in query_result['results']:
        print('\t' + str(result[0]) + ' -----> ' + str(result[1]) + ' %')


# stores query result
sol_1_result['results'] = sol_result(sol_1)
sol_2_result['results'] = sol_result(sol_2)
sol_3_result['results'] = sol_result(sol_3)

# print formatted output
print_results(sol_1_result)
print_results(sol_2_result)
print_error_results(sol_3_result)
