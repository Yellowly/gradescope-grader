# dataclass.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urljoin
from .constants import BASE_URL, Role


@dataclass
class Course:
    '''Represents a course in Gradescope.'''
    course_id: int
    url: str
    role: Role
    term: str
    short_name: str
    full_name: str

    def get_url(self) -> str:
        '''Returns the full URL of the course.'''
        return urljoin(BASE_URL, self.url)


@dataclass
class Assignment:
    '''Represents an assignment in Gradescope.'''
    assignment_id: int
    assignment_type: str
    url: str
    title: str
    container_id: str
    versioned: bool
    version_index: str
    version_name: str
    total_points: str
    student_submission: str
    created_at: str
    release_date: str
    due_date: str
    hard_due_date: str
    time_limit: str
    active_submissions: int
    grading_progress: int
    published: bool
    regrade_requests_open: bool
    regrade_requests_possible: bool
    regrade_request_count: int
    due_or_created_at_date: str

    # Not included:
    # edit_url
    # edit_actions_url
    # has_section_overrides
    # regrade_request_url

    def get_url(self) -> str:
        '''Returns the full URL of the assignment.'''
        return urljoin(BASE_URL, self.url)

    def get_grades_url(self) -> str:
        '''Returns the URL to download the grades for the assignment.'''
        return urljoin(BASE_URL, self.url + '/scores.csv')


@dataclass
class StudentAssignment:
    assignment_id: int
    title: str
    submission_url: str
    template_url: str | None
    submitted: bool
    score: str | None
    release_date: str
    due_date: str
    late_due_date: str | None


@dataclass
class Member:
    '''Represents a member (student or instructor) in Gradescope.'''
    member_id: int
    full_name: str
    first_name: str
    last_name: str
    role: int
    sid: str
    email: str


@dataclass
class Submission:
    '''Represents a submission in Gradescope.'''
    course_id: int
    assignment_id: int
    member_id: int
    submission_id: int
    created_at: str
    score: int
    url: str

    def get_url(self) -> str:
        '''Returns the full URL of the submission.'''
        return urljoin(BASE_URL, self.url)

    def get_file_url(self) -> str:
        '''Returns the URL to download the submission file.'''
        return urljoin(BASE_URL, self.url + '.zip')


@dataclass
class RubricItem:
    id: int
    description: str
    weight: str
    position: int
    question_id: int
    locked: bool | None = None
    group_id: int | None = None
    source_id: int | None = None
    present: bool | None = None
    
    
@dataclass
class ContentItem:
    type: str
    value: str | None = None
    choices: list[dict[str, Any]] | None = None # TODO: create another dataclass for choices


@dataclass
class Question:
    id: int
    parent_id: int | None
    index: int
    type: str
    title: str
    weight: str
    scoring_type: str
    floor: bool
    ceiling: bool
    content: list[ContentItem]
    crop_rect_list: list[Any] | None
    children: list[Question] | None
    full_index: str
    full_answer_key: bool
    
    def get_rubric(self, rubric_items: list[RubricItem]):
        return filter(lambda r: r.question_id == self.id, rubric_items)
    
    def get_child(self, full_index: str):
        if self.children == None:
            raise Exception(f"Question {self.id} has no children")
        return next(filter(lambda q: q.full_index == full_index, self.children))
    
    
@dataclass
class QuestionSubmission:
    question_id: int
    data: dict[str, Any]
    active: bool
    answers: dict[str, str]
    id: int
    score: float | None = None
    evaluations: list[Any] = field(default_factory = list)
    grade_path: str = ""
    annotations: list[Any] = field(default_factory = list)
    
    def get_grader_url(self):
        return urljoin(BASE_URL, self.grade_path)
    
    
@dataclass
class SubmissionViewer:
    submission_id: int
    questions: list[dict[str, Any]]
    question_submissions: list[QuestionSubmission]
    rubric_items: list[RubricItem]
    assignment: dict
    assignment_level_rubric: bool
    assignment_submission: dict
    course_members: list
    current_user: dict
    grades_visible: bool
    hide_email_addresses: bool
    student_hide_email_addresses: bool
    image_attachments: list
    inorder_leaf_question_ids: list
    outline: list
    ownerships: list
    inactive: bool
    past_submissions: list
    paths: dict
    regrade_requests: list
    rubric_item_groups: list
    successful_submission_modal: dict
    text_files: list
    text_annotations_enabled: bool
    rubric_annotation_association_enabled: bool
    quickmarks_enabled: bool
    show_outline_header_message: bool
    container: str | None = None
    pdf_attachment: str | None = None
    successful_submission: str | None = None
    
    def get_question_submission(self, question: Question):
        for s in self.question_submissions:
            if s.question_id == question.id:
                return s
        raise IndexError(f"Could not find question {question.id} in this submission")