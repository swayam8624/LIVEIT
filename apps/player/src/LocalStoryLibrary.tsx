import React, { useEffect, useState } from 'react';
import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { parseStory, type Story } from '@living/story-schema';
import { reunion } from '@living/content';

const KEY = 'liveit:local-stories:v1';
const MAX_STORIES = 12;
const MAX_JSON = 250_000;

/**
 * Offline story-import bridge between Creator Studio's JSON export and
 * the player runtime. This is NOT a public publishing service. No uploaded
 * executable code or arbitrary scripts can run: parseStory validates
 * all scene references, conditions and effect permissions.
 */
export function LocalStoryLibrary({
  onPlay,
}: {
  onPlay: (story: Story) => void;
}) {
  const [stories, setStories] = useState<Story[]>([]);
  const [source, setSource] = useState('');
  const [notice, setNotice] = useState('Paste a Creator Studio JSON export to play it locally.');
  const [open, setOpen] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem(KEY)
      .then((value) => {
        if (value) {
          const items: unknown = JSON.parse(value);
          if (!Array.isArray(items)) throw new Error('Stored library is invalid');
          const valid = items.slice(0, MAX_STORIES).map((item) => parseStory(item));
          setStories(valid);
        }
      })
      .catch(() => setNotice('Stored stories could not be loaded. Original save data is untouched.'))
      .finally(() => setLoaded(true));
  }, []);

  async function importFromText() {
    if (!loaded) return;
    if (source.length > MAX_JSON) {
      setNotice('The story is too large. Limit: 250 KB of JSON.');
      return;
    }
    try {
      const parsed = parseStory(JSON.parse(source));
      if (parsed.id === reunion.id) {
        throw new Error('The original story ID is reserved. Choose another story ID.');
      }
      const next = [...stories.filter((item) => item.id !== parsed.id), parsed];
      if (next.length > MAX_STORIES) throw new Error('Local library limit is 12 stories.');
      await AsyncStorage.setItem(KEY, JSON.stringify(next));
      setStories(next);
      setSource('');
      setOpen(false);
      setNotice('Imported "' + parsed.title + '". Select Play to try it in your current life.');
    } catch (error) {
      setNotice(error instanceof Error ? error.message : 'Invalid story package');
    }
  }

  async function removeStory(id: string) {
    const next = stories.filter((story) => story.id !== id);
    try {
      await AsyncStorage.setItem(KEY, JSON.stringify(next));
      setStories(next);
      setNotice('Removed from this device. Existing journal entries remain in their saves.');
    } catch {
      setNotice('Could not update the local library.');
    }
  }

  return (
    <View style={styles.shelf}>
      <View style={styles.heading}>
        <View style={{ flex: 1 }}>
          <Text style={styles.kicker}>YOUR STORY SHELF</Text>
          <Text style={styles.title}>Play something new.</Text>
        </View>
        <Pressable accessibilityRole="button" onPress={() => setOpen((v) => !v)} style={styles.cta}>
          <Text style={styles.ctaText}>{open ? 'Close import' : '+ Import a story'}</Text>
        </Pressable>
      </View>
      <Text style={styles.help}>Creator Studio exports work offline here. Imported encounters run against your current life, not a global community feed.</Text>
      {open && (
        <View style={styles.importer}>
          <Text style={styles.label}>STORY PACKAGE · JSON</Text>
          <TextInput
            accessibilityLabel="Paste Creator Studio story JSON"
            multiline
            numberOfLines={6}
            value={source}
            onChangeText={setSource}
            style={styles.input}
            placeholder="Paste the exported story JSON here"
            placeholderTextColor="#8794a7"
          />
          <Pressable accessibilityRole="button" style={styles.cta} onPress={() => void importFromText()}>
            <Text style={styles.ctaText}>Validate & save story ↗</Text>
          </Pressable>
        </View>
      )}
      <Text accessibilityLiveRegion="polite" style={styles.notice}>{notice}</Text>
      {!loaded ? <Text style={styles.help}>Loading local stories…</Text> :
        stories.length === 0 ? <Text style={styles.help}>Your shelf is empty. Create a story in Creator Studio and bring it here.</Text> :
          stories.map((story) => (
            <View style={styles.story} key={story.id}>
              <View style={{ flex: 1, gap: 4 }}>
                <Text style={styles.storyTitle}>{story.title}</Text>
                <Text style={styles.help}>{story.description}</Text>
                <Text style={styles.kicker}>{story.scenes.length} SCENES · v{story.version} · LOCAL</Text>
              </View>
              <View style={{ gap: 6 }}>
                <Pressable accessibilityRole="button" onPress={() => onPlay(story)} style={styles.cta}>
                  <Text style={styles.ctaText}>Play ↗</Text>
                </Pressable>
                <Pressable accessibilityRole="button" accessibilityLabel={'Remove ' + story.title} onPress={() => void removeStory(story.id)} style={styles.remove}>
                  <Text style={styles.removeText}>Remove</Text>
                </Pressable>
              </View>
            </View>
          ))
      }
    </View>
  );
}
const styles = StyleSheet.create({
  shelf: { backgroundColor: '#172438', borderColor: '#48516a', borderWidth: 1, padding: 20, borderRadius: 14, gap: 13 },
  heading: { flexDirection: 'row', gap: 12, alignItems: 'center', flexWrap: 'wrap' },
  kicker: { color: '#e4b37b', letterSpacing: 1.6, fontSize: 10, fontWeight: '700' },
  title: { color: '#f8d6ae', fontSize: 27, fontWeight: '700' },
  help: { color: '#bac3d1', fontSize: 12, lineHeight: 19 },
  cta: { backgroundColor: '#945332', borderColor: '#df9b65', borderWidth: 1, paddingHorizontal: 15, paddingVertical: 12, minHeight: 44, justifyContent: 'center', borderRadius: 8 },
  ctaText: { color: '#ffefe0', fontSize: 12, fontWeight: '700', textAlign: 'center' },
  importer: { borderTopWidth: 1, borderColor: '#45516b', paddingTop: 14, gap: 11 },
  input: { minHeight: 130, backgroundColor: '#0d1727', color: '#f9eee4', borderColor: '#516179', borderWidth: 1, borderRadius: 9, padding: 13, textAlignVertical: 'top', fontSize: 12 },
  label: { color: '#dfb484', fontSize: 10, letterSpacing: 1.2 },
  notice: { color: '#e0cba9', fontSize: 12, lineHeight: 18 },
  story: { backgroundColor: '#202e44', borderRadius: 9, borderColor: '#48546a', borderWidth: 1, padding: 14, flexDirection: 'row', gap: 12 },
  storyTitle: { color: '#f5d3a7', fontSize: 17, fontWeight: '700' },
  remove: { padding: 8, alignItems: 'center' },
  removeText: { fontSize: 12, color: '#d1c4bf' },
});
