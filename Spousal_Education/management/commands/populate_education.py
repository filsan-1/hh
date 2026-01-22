from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from Spousal_Education.models import ArticleCategory, EducationalArticle


class Command(BaseCommand):
    help = 'Populate the database with sample educational articles for spouses'

    def handle(self, *args, **kwargs):
        # Get or create an admin user for authoring articles
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create categories
        categories_data = [
            {
                'name': 'Understanding PCOS',
                'icon': '🔬',
                'color': '#FF6B9D',
                'description': 'Learn about Polycystic Ovary Syndrome and how to support your partner'
            },
            {
                'name': 'Endometriosis Guide',
                'icon': '💊',
                'color': '#C44569',
                'description': 'Understanding endometriosis and its impact on daily life'
            },
            {
                'name': 'Menstrual Cycle Phases',
                'icon': '📅',
                'color': '#F8B195',
                'description': 'Understanding the four phases of the menstrual cycle'
            },
            {
                'name': 'Emotional Support',
                'icon': '💝',
                'color': '#9B59B6',
                'description': 'How to provide emotional support during difficult times'
            },
            {
                'name': 'Lifestyle & Diet',
                'icon': '🥗',
                'color': '#26C281',
                'description': 'Nutrition and lifestyle tips for hormonal health'
            },
            {
                'name': 'Communication Tips',
                'icon': '💬',
                'color': '#3498DB',
                'description': 'Effective communication about health and emotions'
            },
        ]

        for cat_data in categories_data:
            category, created = ArticleCategory.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Sample articles
        articles_data = [
            {
                'title': 'What is PCOS? A Guide for Partners',
                'category_slug': 'understanding-pcos',
                'difficulty': 'beginner',
                'read_time': 5,
                'featured': True,
                'summary': 'Polycystic Ovary Syndrome (PCOS) affects 1 in 10 women. Learn what it is, how it impacts your partner, and how you can be supportive.',
                'content': '''Polycystic Ovary Syndrome (PCOS) is a hormonal disorder that affects approximately 10% of women of reproductive age. It's one of the most common causes of female infertility and can have significant impacts on physical and emotional well-being.

**What Happens in PCOS:**
PCOS causes the ovaries to produce excess androgens (male hormones), leading to irregular periods, difficulty getting pregnant, and various other symptoms. The exact cause isn't fully understood, but it involves a combination of genetic and environmental factors.

**Common Symptoms Your Partner May Experience:**
- Irregular or absent menstrual periods
- Excess hair growth on face, chest, or back (hirsutism)
- Weight gain or difficulty losing weight
- Acne and oily skin
- Thinning hair or hair loss
- Dark patches of skin
- Mood changes, anxiety, or depression

**How PCOS Affects Daily Life:**
Women with PCOS often struggle with:
- Physical discomfort and pain
- Body image issues
- Emotional ups and downs due to hormonal fluctuations
- Frustration with weight management
- Concerns about fertility
- Fatigue and low energy

**How You Can Be Supportive:**
1. **Educate Yourself**: Understanding PCOS shows you care and helps you be more empathetic.
2. **Be Patient**: Symptoms can vary day to day. What she can do one day might be difficult the next.
3. **Encourage Healthy Habits**: Support her in maintaining a balanced diet and regular exercise without being pushy.
4. **Listen Without Judgment**: Sometimes she just needs to vent. Listen actively and validate her feelings.
5. **Accompany Her to Appointments**: Offer to go to doctor visits for moral support.
6. **Be Flexible**: Plans might need to change based on how she's feeling.
7. **Show Love Beyond Physical Appearance**: PCOS can affect self-esteem. Remind her of her worth.

**Remember:**
PCOS is a medical condition, not a personal failing. Your support and understanding can make a tremendous difference in how she manages it.''',
                'key_takeaways': '''• PCOS affects 1 in 10 women and is a leading cause of infertility
• It causes hormonal imbalances leading to irregular periods, weight issues, and emotional changes
• Symptoms vary widely and can change day to day
• Your patience, understanding, and support are invaluable
• Encouraging healthy habits without judgment helps
• PCOS is manageable with proper medical care and lifestyle changes'''
            },
            {
                'title': 'Understanding Endometriosis: What Partners Need to Know',
                'category_slug': 'endometriosis-guide',
                'difficulty': 'beginner',
                'read_time': 7,
                'featured': True,
                'summary': 'Endometriosis affects millions of women worldwide. Learn about this painful condition and how to support your partner through it.',
                'content': '''Endometriosis is a condition where tissue similar to the lining of the uterus grows outside the uterus, causing pain and other symptoms. It affects approximately 1 in 10 women during their reproductive years.

**What is Endometriosis:**
Normally, the endometrium (uterine lining) grows inside the uterus and sheds during menstruation. With endometriosis, this tissue grows on ovaries, fallopian tubes, bowels, bladder, or other pelvic areas. During menstruation, this misplaced tissue bleeds but has nowhere to go, causing inflammation, pain, and scar tissue.

**Common Symptoms:**
- Severe menstrual cramps that worsen over time
- Chronic pelvic pain
- Pain during or after intercourse
- Pain with bowel movements or urination during periods
- Heavy or irregular bleeding
- Fatigue
- Digestive issues (diarrhea, constipation, bloating)
- Difficulty getting pregnant

**The Invisible Pain:**
One of the most challenging aspects of endometriosis is that it's an "invisible illness." Your partner may look fine on the outside but be in significant pain. The severity of pain doesn't always correlate with the extent of endometriosis—even small amounts can cause severe pain.

**Impact on Daily Life:**
Endometriosis can affect:
- Work and career (missed days due to pain)
- Social activities and relationships
- Intimate relationships
- Mental health (depression, anxiety)
- Sleep quality
- Overall quality of life

**How to Support Your Partner:**
1. **Believe Her Pain**: Even if you can't see it, the pain is real and valid.
2. **Learn About the Condition**: Understanding helps you empathize better.
3. **Be Present During Flare-Ups**: Heating pads, gentle massages, or just being there can help.
4. **Respect Intimacy Boundaries**: Sex can be painful. Be understanding and communicate openly.
5. **Help With Tasks**: On bad days, help with household chores without being asked.
6. **Encourage Medical Care**: Support her in seeking proper diagnosis and treatment.
7. **Validate Her Emotions**: Living with chronic pain is exhausting. Let her express frustration.
8. **Plan Flexible Dates**: Have backup plans if pain prevents original plans.

**Treatment Options:**
While there's no cure, treatments include:
- Pain medication
- Hormonal therapy
- Surgery (in severe cases)
- Lifestyle modifications
- Alternative therapies (acupuncture, physical therapy)

**Remember:**
Endometriosis is not "just bad periods." It's a serious medical condition that requires understanding, patience, and support from loved ones.''',
                'key_takeaways': '''• Endometriosis causes tissue similar to uterine lining to grow outside the uterus
• It affects 1 in 10 women and causes chronic pain and other symptoms
• Pain is real even when invisible—believe and validate her experience
• It can impact work, social life, intimacy, and mental health
• There's no cure, but various treatments can help manage symptoms
• Your understanding and support make a significant difference'''
            },
            {
                'title': 'The Four Phases of the Menstrual Cycle Explained',
                'category_slug': 'menstrual-cycle-phases',
                'difficulty': 'beginner',
                'read_time': 6,
                'featured': True,
                'summary': 'Understanding the menstrual cycle phases helps you support your partner better. Learn about hormonal changes and their effects.',
                'content': '''The menstrual cycle is more than just the period. It's a complex monthly process involving hormonal changes that affect physical health, emotions, energy levels, and more. Understanding these phases helps you be a more supportive partner.

**The Four Phases:**

**1. Menstrual Phase (Days 1-5):**
This is the period itself, when the uterine lining sheds.

*What's Happening:*
- Hormone levels (estrogen and progesterone) are at their lowest
- Uterine lining breaks down and is expelled
- Energy levels are typically low

*Common Experiences:*
- Cramps and pelvic pain
- Fatigue and need for more rest
- Headaches
- Back pain
- Mood may be low initially but often improves as period progresses
- Some women feel relief that the period has started

*How to Support:*
- Offer heating pads or hot water bottles
- Be understanding if she needs rest or alone time
- Help with household tasks
- Have her favorite comfort foods or treats on hand
- Don't take moodiness personally

**2. Follicular Phase (Days 6-14):**
After menstruation, the body prepares for potential pregnancy.

*What's Happening:*
- Follicle-stimulating hormone (FSH) stimulates egg development
- Estrogen levels rise, rebuilding uterine lining
- One dominant follicle emerges

*Common Experiences:*
- Energy levels increase
- Mood typically improves and stabilizes
- Increased libido
- Better mental clarity and focus
- Skin may look clearer and more radiant
- Feeling more social and outgoing

*How to Support:*
- This is often a great time for activities and dates
- Encourage her interests and hobbies
- Enjoy the increased energy together
- Support her social activities

**3. Ovulation Phase (Around Day 14):**
The egg is released and is available for fertilization.

*What's Happening:*
- Luteinizing hormone (LH) surges, triggering egg release
- Estrogen peaks
- Testosterone also peaks

*Common Experiences:*
- Highest energy levels of the cycle
- Peak libido
- Increased confidence
- May experience mild ovulation pain (mittelschmerz)
- Heightened senses
- Feeling most attractive and social

*How to Support:*
- Great time for physical activities together
- She may be more interested in intimacy
- Appreciate her high energy and positive mood
- Be aware of fertility if you're trying to conceive or prevent pregnancy

**4. Luteal Phase (Days 15-28):**
The body prepares for either pregnancy or menstruation.

*What's Happening:*
- Corpus luteum produces progesterone
- If no pregnancy occurs, progesterone and estrogen drop
- PMS symptoms typically appear in the later part of this phase

*Common Experiences:*
Early Luteal Phase (days 15-22):
- Energy remains relatively good
- Mood is generally stable

Late Luteal Phase/PMS (days 23-28):
- Energy decreases
- Mood changes (irritability, anxiety, sadness)
- Physical symptoms: bloating, breast tenderness, headaches, cravings
- Difficulty concentrating
- Increased need for sleep
- Social withdrawal

*How to Support:*
- Be extra patient and understanding
- Don't take mood swings personally—it's hormones
- Help reduce her stress
- Be mindful of her cravings without judgment
- Give her space when needed
- Offer massages or other comfort measures
- Remember it's temporary

**General Tips for All Phases:**

1. **Track the Cycle Together**: Use a period tracking app to anticipate needs.

2. **Communication is Key**: Ask how she's feeling and what she needs.

3. **Don't Blame Everything on Hormones**: While hormones affect mood, legitimate concerns are still valid.

4. **Maintain Consistency**: Show love and support throughout all phases, not just during difficult times.

5. **Educate Yourself**: The more you understand, the better partner you can be.

**Remember:**
Every woman's cycle is unique. These are general patterns, but experiences vary. The most important thing is to communicate openly with your partner about her specific needs and experiences.''',
                'key_takeaways': '''• The menstrual cycle has 4 distinct phases, each with different hormonal patterns
• Energy, mood, and physical symptoms vary throughout the cycle
• Menstrual phase: Low energy, needs comfort and understanding
• Follicular phase: Rising energy, good time for activities
• Ovulation: Peak energy and libido
• Luteal phase: PMS symptoms in later days, needs extra patience
• Understanding the cycle helps you anticipate and meet her needs
• Communication and tracking together strengthen your support'''
            },
            {
                'title': 'How to Support Your Partner Through PMS',
                'category_slug': 'emotional-support',
                'difficulty': 'beginner',
                'read_time': 5,
                'featured': False,
                'summary': 'PMS affects 90% of women. Learn practical ways to support your partner during this challenging time each month.',
                'content': '''Premenstrual Syndrome (PMS) affects up to 90% of menstruating women to some degree. For some, it's mild, while others experience significant physical and emotional symptoms. Understanding and supporting your partner through PMS strengthens your relationship.

**What is PMS?**
PMS refers to physical and emotional symptoms that occur in the one to two weeks before menstruation. It's caused by hormonal changes, particularly the drop in estrogen and progesterone before the period starts.

**Common PMS Symptoms:**

Physical:
- Bloating and water retention
- Breast tenderness and swelling
- Headaches or migraines
- Fatigue
- Food cravings (especially for sweets or salty foods)
- Digestive issues
- Muscle aches
- Acne breakouts

Emotional/Mental:
- Mood swings
- Irritability and anger
- Anxiety or tension
- Depression or sadness
- Difficulty concentrating
- Social withdrawal
- Changes in sleep patterns
- Decreased libido

**Why PMS Causes Mood Changes:**
It's not "all in her head." The hormonal fluctuations before menstruation affect neurotransmitters like serotonin, which regulates mood. Lower serotonin levels can cause irritability, depression, and food cravings. Understanding this helps you not take mood changes personally.

**What NOT to Do:**
❌ Say "Are you on your period?" or "You're just being hormonal"
❌ Dismiss her feelings as invalid or exaggerated
❌ Take her irritability as a personal attack
❌ Make jokes about PMS
❌ Expect her to "just deal with it"
❌ Act like this happens to everyone the same way

**What TO Do:**

**1. Acknowledge Her Feelings:**
"I can see you're having a tough time. Is there anything I can do to help?"

**2. Create a Comfortable Environment:**
- Adjust room temperature (she may feel warmer due to bloating)
- Dim lights if she has a headache
- Reduce noise and create calm spaces
- Have heating pads ready for cramps

**3. Help With Practical Tasks:**
- Take over cooking dinner
- Handle household chores without being asked
- Run errands
- Take care of kids if you have them
- Create one less thing for her to worry about

**4. Offer Physical Comfort:**
- Gentle back or foot massages
- Cuddle if she wants closeness
- Respect if she needs space
- Light touch can be soothing

**5. Food Support:**
- Have her favorite snacks available
- Don't judge her cravings
- Prepare or bring her favorite comfort foods
- Keep chocolate in the house (really, this helps!)
- Ensure healthy options are also available

**6. Exercise Patience:**
- She knows she's irritable and probably feels bad about it
- Don't engage in arguments during this time if possible
- Give extra grace and understanding
- Remember it's temporary—usually 7-10 days max

**7. Maintain Open Communication:**
- Ask: "What do you need from me right now?"
- Listen without trying to "fix" everything
- Validate: "That sounds really frustrating"
- Check in: "How are you feeling today?"

**8. Learn Her Patterns:**
- Track her cycle (with her permission) to anticipate PMS
- Notice what helps and what doesn't
- Every woman is different; learn what works for her

**9. Encourage Self-Care:**
- Support her in taking time for herself
- Encourage activities that help (warm bath, reading, etc.)
- Don't add to her guilt if she needs to slow down

**10. Know When to Seek Help:**
If symptoms are severe (PMDD - Premenstrual Dysphoric Disorder):
- Significant depression or anxiety
- Severe mood swings affecting daily life
- Suicidal thoughts
- Inability to function normally
Encourage her to see a healthcare provider. Treatment options are available.

**Long-Term Support:**
- Regular exercise together (helps reduce PMS)
- Support healthy eating habits
- Reduce stress in your shared life
- Encourage adequate sleep
- Consider vitamin supplements (B6, magnesium, calcium) under doctor guidance

**For Your Own Well-Being:**
Supporting someone through PMS can be challenging. Remember:
- Take breaks when you need them
- Don't absorb her emotions—maintain healthy boundaries
- Seek support from friends if needed
- Practice patience and remember it's temporary
- Focus on your love for her and desire to help

**Remember:**
Your support during PMS shows your commitment to the relationship and your partner's well-being. Small acts of kindness during this time make a huge difference and strengthen your bond.''',
                'key_takeaways': '''• PMS affects up to 90% of women with varying severity
• Symptoms are caused by real hormonal changes, not imagination
• Never dismiss her feelings or make "period" jokes
• Practical help (chores, errands, food) is incredibly valuable
• Patience and understanding during mood swings are crucial
• Track her cycle to anticipate and prepare for PMS
• Severe symptoms (PMDD) require professional medical help
• Your support during difficult times strengthens your relationship'''
            },
            {
                'title': 'Nutrition Tips for Hormonal Health',
                'category_slug': 'lifestyle-diet',
                'difficulty': 'intermediate',
                'read_time': 8,
                'featured': False,
                'summary': 'Learn how diet impacts hormonal health and how you can support your partner in making beneficial nutritional choices.',
                'content': '''Nutrition plays a crucial role in hormonal health. What we eat can either support hormonal balance or contribute to imbalances. As a supportive partner, understanding these connections helps you encourage healthy habits without being pushy.

**The Diet-Hormone Connection:**

Hormones are chemical messengers that regulate everything from mood to metabolism, sleep to reproduction. They're produced from nutrients we eat, so diet directly affects hormonal health. Poor nutrition can worsen conditions like PCOS, endometriosis, PMS, and irregular cycles.

**Foods That Support Hormonal Health:**

**1. Healthy Fats:**
Essential for hormone production.
- Avocados
- Olive oil
- Nuts (especially walnuts, almonds)
- Seeds (flaxseeds, chia seeds)
- Fatty fish (salmon, sardines, mackerel)
- Coconut oil

*Why They Help:* Hormones are made from cholesterol and fats. Healthy fats provide building blocks for hormone production and help reduce inflammation.

**2. Cruciferous Vegetables:**
Help metabolize estrogen.
- Broccoli
- Cauliflower
- Brussels sprouts
- Cabbage
- Kale

*Why They Help:* Contain compounds that support liver detoxification of excess estrogen, helping maintain hormonal balance.

**3. Fiber-Rich Foods:**
Help eliminate excess hormones.
- Whole grains (quinoa, brown rice, oats)
- Legumes (beans, lentils)
- Vegetables
- Fruits (especially berries, pears, apples)

*Why They Help:* Fiber binds to excess estrogen in the digestive tract and helps eliminate it, preventing reabsorption.

**4. Protein:**
Stabilizes blood sugar and provides amino acids.
- Lean meats (chicken, turkey)
- Fish
- Eggs
- Greek yogurt
- Plant proteins (beans, tofu, tempeh)

*Why They Help:* Protein stabilizes blood sugar, which is crucial for hormonal balance. It also provides amino acids needed for hormone production.

**5. Antioxidant-Rich Foods:**
Reduce inflammation and oxidative stress.
- Berries (blueberries, strawberries, raspberries)
- Dark chocolate (70%+ cacao)
- Green tea
- Colorful vegetables
- Herbs and spices (turmeric, ginger)

*Why They Help:* Reduce inflammation that can disrupt hormonal signaling.

**Foods to Limit:**

**1. Refined Sugar and Carbs:**
- White bread, pastries
- Sugary drinks
- Candy and sweets
- Processed snacks

*Why:* Cause blood sugar spikes and crashes, leading to insulin resistance, which disrupts other hormones.

**2. Processed Foods:**
- Fast food
- Packaged meals
- Processed meats

*Why:* Often contain trans fats, excess sodium, and preservatives that promote inflammation.

**3. Excessive Caffeine:**
- More than 200-300mg daily (2-3 cups coffee)

*Why:* Too much can increase cortisol (stress hormone) and disrupt sleep, affecting other hormones.

**4. Alcohol:**
- Especially in excess

*Why:* Liver metabolizes both alcohol and hormones. Excess alcohol burden impairs hormone metabolism.

**5. Dairy (for some women):**
- Especially conventional dairy with hormones

*Why:* Can trigger inflammation in sensitive individuals and contains hormones that may disrupt balance.

**Specific Conditions:**

**For PCOS:**
- Focus on low-glycemic index foods
- Increase anti-inflammatory foods
- Consider reducing dairy
- Add cinnamon (helps insulin sensitivity)
- Include spearmint tea (may help with excess androgens)

**For Endometriosis:**
- Anti-inflammatory diet is key
- Omega-3 rich foods
- Avoid red meat and processed meats
- Limit alcohol
- Consider eliminating gluten (helps some women)

**For PMS:**
- Reduce salt to minimize bloating
- Increase magnesium-rich foods (dark chocolate, nuts, leafy greens)
- Complex carbs for serotonin production
- Avoid excessive caffeine
- Include B-vitamin rich foods

**How to Support Healthy Eating:**

**1. Cook Together:**
Make healthy eating a shared activity, not a burden she faces alone. Try new recipes together on weekends.

**2. Stock the Kitchen:**
Keep healthy options readily available. If it's in the house, it's easier to eat it.

**3. Meal Prep Together:**
Prepare meals in advance for busy weeks. This removes the decision-making burden when she's tired.

**4. Lead by Example:**
Eat healthy yourself. Don't expect her to eat salad while you eat pizza. Make it a shared lifestyle.

**5. Make It Enjoyable:**
Healthy food doesn't have to be boring. Experiment with flavors, herbs, and cooking methods.

**6. Don't Be the Food Police:**
Support, don't criticize. If she wants chocolate during PMS, don't shame her. Balance is key.

**7. Celebrate Non-Food Victories:**
Don't always use food as reward or comfort. Find other ways to celebrate and cope with emotions.

**8. Learn Together:**
Read about nutrition, watch documentaries, attend cooking classes together.

**9. Be Patient with Changes:**
Dietary changes take time. Support the journey, not just the destination.

**10. Respect Her Choices:**
Ultimately, it's her body and her choice. You can support, but not control.

**Practical Meal Ideas:**

**Breakfast:**
- Greek yogurt with berries, nuts, and chia seeds
- Veggie omelet with avocado
- Oatmeal with almond butter and fruit
- Smoothie with spinach, berries, protein powder, flaxseeds

**Lunch:**
- Quinoa bowl with roasted vegetables and salmon
- Large salad with mixed greens, chicken, nuts, and olive oil dressing
- Lentil soup with whole grain bread
- Veggie-packed stir-fry with brown rice

**Dinner:**
- Baked salmon with roasted broccoli and sweet potato
- Turkey chili with beans and vegetables
- Chicken with cauliflower rice and mixed vegetables
- Tofu stir-fry with plenty of colorful veggies

**Snacks:**
- Apple with almond butter
- Hummus with vegetable sticks
- Trail mix (nuts and seeds, minimal sugar)
- Dark chocolate squares (70%+ cacao)
- Hard-boiled eggs

**Supplements to Consider:**
(Always consult with a healthcare provider first)
- Omega-3 fish oil
- Vitamin D
- B-complex vitamins
- Magnesium
- Probiotics
- Inositol (especially for PCOS)

**Remember:**
Nutrition is one tool in the toolbox for hormonal health. It's not about perfection, but consistent, balanced choices. Some days will be better than others, and that's okay. Your support in creating a healthy food environment makes a significant difference.

**Final Thoughts:**
Food is deeply emotional and social. Approach nutrition support with empathy, not judgment. The goal is health and well-being, not rigid rules or restriction. Make it a journey you take together, celebrating small victories along the way.''',
                'key_takeaways': '''• Diet significantly impacts hormonal health and balance
• Healthy fats, fiber, protein, and antioxidants support hormones
• Limit refined sugar, processed foods, and excessive caffeine
• Different conditions benefit from specific dietary approaches
• Cook and meal prep together to make healthy eating easier
• Support without being controlling or judgmental
• Lead by example with your own food choices
• Focus on progress, not perfection
• Consult healthcare providers before starting supplements'''
            },
            {
                'title': 'Communicating About Health: Tips for Partners',
                'category_slug': 'communication-tips',
                'difficulty': 'beginner',
                'read_time': 6,
                'featured': False,
                'summary': 'Effective communication about health issues strengthens relationships. Learn how to talk about sensitive topics with care and understanding.',
                'content': '''Open, honest communication about health—especially reproductive health—can be challenging but is essential for a strong, supportive relationship. Learning to discuss these topics with sensitivity and care creates deeper intimacy and trust.

**Why Communication Matters:**

When women face hormonal health issues like PCOS, endometriosis, or difficult periods, they often feel isolated, misunderstood, or embarrassed. Your willingness to engage in open dialogue shows:
- You care about her well-being
- You're a safe person to be vulnerable with
- You're committed to understanding her experience
- You value her beyond physical aspects

**Common Communication Barriers:**

**1. Embarrassment:**
Many people feel awkward discussing reproductive health, menstruation, or related symptoms.

**2. Lack of Knowledge:**
Not knowing the right words or questions can prevent conversations.

**3. Fear of Saying the Wrong Thing:**
Worry about being insensitive can lead to avoiding the topic entirely.

**4. Cultural Taboos:**
Some cultures or families don't openly discuss these topics.

**5. Gender Differences:**
Men may not understand women's health experiences and vice versa.

**6. Minimization of Symptoms:**
Past experiences of being dismissed may make her hesitant to share.

**Breaking Down Barriers:**

**Start Small:**
You don't need to dive into deep discussions immediately. Start with simple check-ins:
- "How are you feeling today?"
- "Is there anything you need?"
- "Are you in any pain?"

**Create Safe Spaces:**
- Choose private, comfortable settings for deeper conversations
- Ensure you have time and won't be interrupted
- Turn off distractions (phones, TV)
- Make it clear you're fully present and listening

**Effective Communication Strategies:**

**1. Ask Open-Ended Questions:**
Instead of: "Are you okay?"
Try: "How are you feeling, and is there anything I can do to help?"

Instead of: "Is your period bad this month?"
Try: "How has your cycle been treating you lately?"

**2. Listen Actively:**
- Make eye contact
- Nod and show you're engaged
- Don't interrupt
- Ask follow-up questions
- Reflect back what you heard: "So it sounds like..."

**3. Validate Her Experience:**
Never say:
- "It can't be that bad"
- "Other women deal with it fine"
- "You're being dramatic"
- "Just tough it out"

Instead say:
- "That sounds really difficult"
- "I'm sorry you're going through this"
- "I believe you"
- "Thank you for sharing that with me"

**4. Ask What She Needs:**
Don't assume. Different situations call for different responses.
- "What would be most helpful right now?"
- "Do you want me to help, or would you prefer space?"
- "Would you like me to just listen, or do you want suggestions?"

**5. Educate Yourself:**
Don't expect her to be your only source of information.
- Read articles (like this one!)
- Watch educational videos
- Ask appropriate questions at appropriate times
- Learn medical terminology

**6. Respect Boundaries:**
If she doesn't want to talk about something, respect that.
- "I'm here if you ever want to talk about it"
- Don't push for details she's not comfortable sharing
- Recognize that some things may be private

**7. Use Appropriate Language:**
- Don't use childish or crude terms for body parts or functions
- Use medical terms when appropriate
- Follow her lead on terminology
- Ask what words she's comfortable with

**Specific Conversation Topics:**

**Discussing Symptoms:**
"I've noticed you've been [tired/in pain/stressed] lately. Do you want to talk about what's going on?"

**Offering Support:**
"I've been learning about [PCOS/endometriosis/etc.], and I want to support you better. What can I do?"

**Addressing Changes in Intimacy:**
"I've noticed our physical intimacy has changed. Is everything okay? Is there pain or discomfort we should talk about?"

**Planning and Scheduling:**
"I know your cycle affects how you feel. Would it help if we planned activities around that?"

**Medical Appointments:**
"Do you want company at your doctor's appointment? I'm happy to go for support if you'd like."

**What NOT to Say:**

❌ "You're being overly emotional" (dismissive)
❌ "That's just how women are" (stereotyping)
❌ "At least it's not [worse condition]" (minimizing)
❌ "Have you tried just not thinking about it?" (invalidating)
❌ "My ex never had these problems" (comparison)
❌ "When will you feel better?" (pressure)
❌ "Let me know if you need anything" without following through (empty offer)

**Better Alternatives:**

✓ "Your feelings are valid"
✓ "I'm here for you"
✓ "That must be really challenging"
✓ "What helps you feel better?"
✓ "I'm learning more about this to understand better"
✓ "There's no rush to feel better; I'm patient"
✓ "I'll bring you [specific thing] later" (concrete offer)

**Navigating Difficult Conversations:**

**When She's Frustrated:**
- Let her vent without trying to fix everything
- Acknowledge the frustration
- Don't take it personally if she's irritable
- Offer comfort when appropriate

**When She's Sad or Depressed:**
- Sit with her in the feeling
- Don't rush to cheer her up
- Validate that her feelings make sense
- Encourage professional help if symptoms are severe or persistent

**When She's Embarrassed:**
- Normalize the conversation
- Share that you're learning and not judging
- Use matter-of-fact tone
- Reassure her there's nothing to be embarrassed about

**When Discussing Fertility Concerns:**
- This is sensitive territory—approach with extra care
- Listen more than you talk
- Validate fears and concerns
- Discuss together, don't make unilateral decisions
- Consider couples counseling if needed

**Building Communication Skills Together:**

**Regular Check-Ins:**
Make health discussions a normal part of your relationship.
- Weekly: "How was your week health-wise?"
- Monthly: "Is there anything coming up with your cycle I should know about?"
- Yearly: "How are your health goals going?"

**Use "We" Language:**
"We're dealing with PCOS" (not "You have PCOS")
"We're working on this together"

This shows partnership and shared responsibility.

**Create Rituals:**
- Nightly check-ins before bed
- Morning "how are you feeling?" conversations
- Regular date nights where deeper topics can arise naturally

**Seek Outside Resources Together:**
- Attend medical appointments together (if she wants)
- Watch educational videos together
- Read books about women's health
- Consider couples therapy if communication is difficult

**Practice Empathy:**

Try to imagine:
- Having monthly pain that significantly impacts your life
- Dealing with symptoms that others can't see
- Worrying about fertility
- Managing a chronic condition
- Feeling judged or dismissed by healthcare providers
- Struggling with body changes beyond your control

This perspective helps you communicate with more compassion.

**When You Make Mistakes:**

You will say the wrong thing sometimes. That's okay.

When it happens:
1. Apologize sincerely: "I'm sorry, that wasn't helpful/supportive"
2. Ask for feedback: "What would have been better to say?"
3. Learn from it
4. Don't be defensive
5. Try again

**Long-Term Benefits:**

Improving communication about health leads to:
- Deeper emotional intimacy
- Greater trust
- Better problem-solving together
- Reduced conflict
- Improved mental health for both partners
- Stronger relationship overall

**Remember:**

Communication is a skill that improves with practice. Be patient with yourself and your partner as you learn to navigate these conversations. The fact that you're reading this article shows you care, and that's the most important foundation for effective communication.

**Final Thought:**

Your partner doesn't need you to fully understand her experience—that's impossible. What she needs is for you to try to understand, to believe her, to support her, and to be willing to have these conversations. That willingness to engage, even when it's uncomfortable, makes all the difference.''',
                'key_takeaways': '''• Open communication about health strengthens relationships and builds trust
• Start with simple check-ins and create safe, private spaces for deeper talks
• Listen actively without interrupting or trying to "fix" everything
• Validate her experience—never dismiss or minimize her symptoms
• Ask what she needs rather than assuming
• Educate yourself independently; don't rely solely on her to teach you
• Use appropriate language and respect her boundaries
• Apologize when you make mistakes and learn from them
• Regular health check-ins normalize these important conversations
• Your willingness to try is what matters most'''
            },
        ]

        for article_data in articles_data:
            category = ArticleCategory.objects.get(slug=article_data['category_slug'])
            article, created = EducationalArticle.objects.get_or_create(
                slug=slugify(article_data['title']),
                defaults={
                    'title': article_data['title'],
                    'category': category,
                    'author': admin_user,
                    'difficulty_level': article_data['difficulty'],
                    'estimated_read_time': article_data['read_time'],
                    'featured': article_data['featured'],
                    'summary': article_data['summary'],
                    'content': article_data['content'],
                    'key_takeaways': article_data['key_takeaways'],
                    'is_published': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created article: {article.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated educational articles!'))
