from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from opaque_keys.edx.keys import CourseKey


def _insert_skill_tags(results):
        # get skill tags for each course
        course_skill_tags = [{'index': idx, 'skill_tags': CourseOverview.get_from_id(CourseKey.from_string(
                       course['_id'])).skill_tags} for idx, course in enumerate(results['results'])]

        # add skill tags to each course in results 
        for course in course_skill_tags:
            if course['skill_tags']:
                skill_tags = [skill_tag.strip() for skill_tag in course['skill_tags'].split(',')]
            else:
                skill_tags = []
            results['results'][course['index']]['data'][u'skill tags'] = skill_tags

def _update_facet(results, facet_key):
        results['facets'][facet_key]['total'] = results['total']
        results['facets'][facet_key]['other'] = 0

        terms_dict = {}
        for course in results['results']:
            course_facet_value = course['data'][facet_key]
            if type(course_facet_value) is not list:
                course_facet_value = [course_facet_value]
            for value in course_facet_value:
                try:
                    terms_dict[value] += 1
                except KeyError:
                    terms_dict[value] = 1

        results['facets'][facet_key]['terms'] = terms_dict

def _update_results(results):
        results['total'] = len(results['results'])

        for facet, value_dict in results['facets'].iteritems():
            _update_facet(results, facet)

def add_skill_facet(results):
        try:
            if 'skill tags' not in results['results'][0]['data']:
                _insert_skill_tags(results)
            skill_tags_dict = {u'skill tags': {'total': 0, 'other': 0, 'terms': {}}}
            results['facets'].update(skill_tags_dict)
            _update_facet(results, 'skill tags')
        except IndexError:
            # if there are no results
            pass

def filter_by_skills(results, selected_skills):
        _insert_skill_tags(results)
        for course in list(results['results']):
            print course['data']['skill tags']
            if selected_skills not in course['data']['skill tags']:
                results['results'].remove(course)

        _update_results(results)

