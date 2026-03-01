from schemas.tasks.match_word2audio import MatchWordAudio
from schemas.tasks.match_word_explanation import MatchWordExplanation
from schemas.tasks.no_new_words import NoNewWords
from schemas.tasks.sentence_with_placeholder import SentenceWithPlaceholder
from schemas.tasks.uncover_task import UncoverTask
from schemas.tasks.word2explanation import Word2Explanation

TaskType = (
    Word2Explanation
    | SentenceWithPlaceholder
    | MatchWordExplanation
    | MatchWordAudio
    | NoNewWords
    | UncoverTask
)
