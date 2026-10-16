import { parseStory } from '@living/story-schema';
const memory = (fact: string, text: string) => ({
  operation: 'add_memory' as const,
  target: 'amelia',
  fact,
  text,
});
const trust = (value: number) => ({
  operation: 'adjust_relationship' as const,
  target: 'amelia',
  value,
});
export const reunion = parseStory({
  schemaVersion: 1,
  id: 'official.the-space-between',
  version: 1,
  title: 'The Space Between',
  description:
    'An old friend. An unfinished conversation. Some things follow you to a new city.',
  compatibleWorlds: ['modern_life_v1'],
  minAge: 18,
  permissions: { relationshipTargets: ['amelia'], memoryTargets: ['amelia'] },
  entry: 'arrival',
  scenes: [
    {
      id: 'arrival',
      speaker: 'Amelia',
      mood: 'reflective',
      text: 'I kept almost calling you. And then a month became a year. Funny how that happens. I didn’t think you’d come.',
      ending: false,
      choices: [
        {
          id: 'apologize',
          label: '“I should have called. I’m sorry.”',
          next: 'honesty',
          conditions: [],
          effects: [
            trust(12),
            memory(
              'apologized',
              'You took responsibility for the silence between you and Amelia.',
            ),
          ],
        },
        {
          id: 'listen',
          label: '“I’m here now. Tell me how you’ve been.”',
          next: 'listening',
          conditions: [],
          effects: [
            trust(6),
            memory(
              'listened',
              'You made space for Amelia to tell her side of the story.',
            ),
          ],
        },
        {
          id: 'guarded',
          label: '“You stopped calling too.”',
          next: 'distance',
          conditions: [],
          effects: [
            trust(-8),
            memory(
              'guarded',
              'Old hurt resurfaced when you met Amelia at the café.',
            ),
          ],
        },
      ],
    },
    {
      id: 'honesty',
      speaker: 'Amelia',
      mood: 'warm',
      text: 'Thank you for saying that. I thought I’d rehearsed this conversation a hundred times, but I never got past the first sentence. What happened to us?',
      ending: false,
      choices: [
        {
          id: 'truth',
          label: '“I was afraid I’d let you down.”',
          next: 'reconnected',
          conditions: [],
          effects: [
            trust(10),
            memory(
              'honest_reunion',
              'You told Amelia the truth. The friendship has a way forward.',
            ),
          ],
        },
        {
          id: 'coffee',
          label: '“Can we start with coffee, and take our time?”',
          next: 'slow',
          conditions: [],
          effects: [
            trust(5),
            memory(
              'coffee_again',
              'You and Amelia agreed to rebuild slowly, one coffee at a time.',
            ),
          ],
        },
      ],
    },
    {
      id: 'listening',
      speaker: 'Amelia',
      mood: 'reflective',
      text: 'I’m opening a little bookshop. Terrifying, honestly. I wanted you to hear it from me. There’s a launch next week, if you want to come.',
      ending: false,
      choices: [
        {
          id: 'support',
          label: '“I wouldn’t miss it.”',
          next: 'reconnected',
          conditions: [],
          effects: [
            trust(10),
            memory(
              'bookshop_invitation',
              'Amelia invited you to her bookshop opening. You promised to be there.',
            ),
          ],
        },
        {
          id: 'explain',
          label: '“Before that, I owe you an explanation.”',
          next: 'honesty',
          conditions: [],
          effects: [trust(4)],
        },
      ],
    },
    {
      id: 'distance',
      speaker: 'Amelia',
      mood: 'tense',
      text: 'You’re right. I did. I guess I hoped one of us would be brave enough to break the silence. We can keep score, or we can try something else.',
      ending: false,
      choices: [
        {
          id: 'repair',
          label: '“I don’t want to keep score anymore.”',
          next: 'slow',
          conditions: [],
          effects: [
            trust(8),
            memory(
              'chose_repair',
              'Despite a difficult start, you chose to give your friendship another chance.',
            ),
          ],
        },
        {
          id: 'leave',
          label: '“Maybe we both need more time.”',
          next: 'apart',
          conditions: [],
          effects: [
            memory(
              'needed_space',
              'You and Amelia parted kindly, but the distance remains.',
            ),
          ],
        },
      ],
    },
    {
      id: 'reconnected',
      speaker: 'Amelia',
      mood: 'warm',
      text: 'Then let’s not wait another year. Outside, the rain has stopped. For the first time since moving here, this city feels a little more like home.',
      ending: true,
      choices: [],
    },
    {
      id: 'slow',
      speaker: 'Amelia',
      mood: 'warm',
      text: 'One coffee at a time. I can do that. She smiles, just a little. Some beginnings are quiet enough that you almost miss them.',
      ending: true,
      choices: [],
    },
    {
      id: 'apart',
      speaker: 'Amelia',
      mood: 'reflective',
      text: 'Take care of yourself, okay? Her cup is still half full when you leave. Not every reunion is a return. Sometimes it’s a place to pause.',
      ending: true,
      choices: [],
    },
  ],
});

/**
 * Second original playable story, created specifically for LIVEIT.
 * Triggered as a follow-up once the first reunion is resolved.
 * Choices carry forward into the existing Amelia relationship and memory log.
 */
export const bookshop = parseStory({
  schemaVersion: 1,
  id: 'official.the-bookshop',
  version: 1,
  title: 'A Place for Second Chances',
  description: 'The opening night of Amelia’s bookshop. Old friendships and new obligations collide.',
  compatibleWorlds: ['modern_life_v1'],
  minAge: 18,
  permissions: { relationshipTargets: ['amelia'], memoryTargets: ['amelia'] },
  entry: 'doorway',
  scenes: [
    {
      id: 'doorway', speaker: 'Amelia', mood: 'reflective',
      text: 'The brass bell above the door rings. Amelia stands behind a stack of books, pencil tucked behind one ear. "You made it. I wasn’t sure you would."',
      ending: false, choices: [
        { id: 'early', label: '"I said I would. What needs doing?"', next: 'backroom', conditions: [], effects: [trust(5), memory('bookshop_early','You arrived early and offered to help Amelia open her bookshop.')] },
        { id: 'look', label: '"I wanted to see what you built."', next: 'aisle', conditions: [], effects: [trust(2)] },
        { id: 'carry', label: '"That stack looks dangerous. Let me help."', next: 'rush', conditions: [], effects: [trust(4)] },
      ],
    },
    {
      id: 'backroom', speaker: 'Amelia', mood: 'warm',
      text: '"That box goes under the window. And please don’t look at the ledger." She looks exhausted, and for a moment she resembles the girl you studied with years ago.',
      ending: false, choices: [
        { id: 'ledger', label: '"You can tell me if things are hard."', next: 'customer', conditions: [], effects: [trust(5)] },
        { id: 'joke', label: '"I promise I only judge terrible book titles."', next: 'opening', conditions: [], effects: [trust(3)] },
      ],
    },
    {
      id: 'aisle', speaker: 'Amelia', mood: 'reflective',
      text: 'Books in three languages line the narrow aisle. A child is already reading on the floor. "I wanted people to feel welcome, even if they came in just to be somewhere warm."',
      ending: false, choices: [
        { id: 'admire', label: '"Then you’ve already succeeded."', next: 'opening', conditions: [], effects: [trust(4)] },
        { id: 'remember', label: '"You used to draw floor plans in lectures."', next: 'quiet', conditions: [], effects: [memory('bookshop_old_days','You remembered the plans Amelia used to sketch in university.')] },
      ],
    },
    {
      id: 'rush', speaker: 'Amelia', mood: 'tense',
      text: 'A tower of books topples beside a customer. You catch most of them. Amelia stands frozen for a second before whispering, "I have no idea what I’m doing."',
      ending: false, choices: [
        { id: 'steady', label: '"You don’t have to know everything tonight."', next: 'opening', conditions: [], effects: [trust(6)] },
        { id: 'organize', label: '"I’ll handle the queue. Take a minute."', next: 'crisis', conditions: [], effects: [trust(4)] },
      ],
    },
    {
      id: 'customer', speaker: 'Narrator', mood: 'reflective',
      text: 'A customer wants a signed first edition that was promised but never delivered. Behind the counter, Amelia’s hands tremble slightly.',
      ending: false, choices: [
        { id: 'admit', label: 'Explain the mistake honestly', next: 'opening', conditions: [], effects: [trust(4), memory('bookshop_honesty','You helped Amelia handle a disappointed customer honestly.')] },
        { id: 'improvise', label: 'Offer another book and a personal note', next: 'quiet', conditions: [], effects: [trust(2)] },
      ],
    },
    {
      id: 'opening', speaker: 'Amelia', mood: 'warm',
      text: 'By eight o’clock the shop is crowded. Someone raises a glass. Amelia catches your eye over the heads of strangers, then turns to give the briefest speech you have ever heard.',
      ending: false, choices: [
        { id: 'cheer', label: 'Join the crowd celebrating her work', next: 'grand_opening', conditions: [], effects: [trust(6), memory('bookshop_celebration','You stood beside Amelia as the bookshop came alive.')] },
        { id: 'after', label: 'Stay to help when the guests leave', next: 'late_night', conditions: [], effects: [trust(8), memory('bookshop_afterhours','You remained after closing to help Amelia finish the evening.')] },
      ],
    },
    {
      id: 'quiet', speaker: 'Amelia', mood: 'reflective',
      text: 'You find her by the back window after the crowd thins. "I built this place because I was tired of being afraid. Funny how opening it made me afraid all over again."',
      ending: false, choices: [
        { id: 'sit', label: '"Then I’ll sit with you for a little while."', next: 'late_night', conditions: [], effects: [trust(6)] },
        { id: 'goodbye', label: '"You should be proud. I’ll leave you to it."', next: 'separate', conditions: [], effects: [trust(1)] },
      ],
    },
    {
      id: 'crisis', speaker: 'Amelia', mood: 'tense',
      text: 'The card machine stops working. A customer complains loudly. You can take charge of the crowd, but Amelia has already asked everyone to be patient.',
      ending: false, choices: [
        { id: 'back', label: 'Back up her decision', next: 'grand_opening', conditions: [], effects: [trust(5)] },
        { id: 'takeover', label: 'Take over the situation yourself', next: 'separate', conditions: [], effects: [trust(-5), memory('bookshop_boundaries','You overstepped while trying to rescue the opening night.')] },
      ],
    },
    {
      id: 'grand_opening', speaker: 'Amelia', mood: 'warm',
      text: '"Thank you," she says as the final guests leave. The bell above the door rings one last time. A city can feel enormous until someone makes a little place for you in it.',
      ending: true, choices: [],
    },
    {
      id: 'late_night', speaker: 'Amelia', mood: 'warm',
      text: 'You finish stacking chairs long after midnight. She switches off the sign, leaving only the reading lamps. Neither of you rushes toward the door.',
      ending: true, choices: [],
    },
    {
      id: 'separate', speaker: 'Narrator', mood: 'reflective',
      text: 'From across the street, the windows glow like a lantern. You leave Amelia to her new life, knowing that caring for someone does not always mean being beside them.',
      ending: true, choices: [],
    },
  ],
});

/** Bundled stories can always be resumed offline without a local story import. */
export const OFFICIAL_STORIES = [reunion, bookshop] as const;
export function findOfficialStory(id: string) {
  return OFFICIAL_STORIES.find(story => story.id === id);
}
