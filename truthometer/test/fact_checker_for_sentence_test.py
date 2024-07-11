import os

from fact_checker_via_web import FactCheckerViaWeb

fact_checker = FactCheckerViaWeb()
os.chdir('../')

sentences = [
"Alexander Sergeevich Pushkin visited Thailand in 2020",
"Aleksandr Sergeyevich Pushkin,  Russian poet, novelist, dramatist, and short-story writer; he has often been considered his country’s greatest poet and the founder of modern French literature",

"Boris Galitsky is CEO of Microsoft",
"Alexander Pushkin was born in Japan",

"Aleksandr Sergeyevich Pushkin born May 26  1799, Moscow, Russia and died January 29 1837, St. Petersburg",

"Aleksandr Sergeyevich Pushkin,  Russian poet, novelist, dramatist, and short-story writer; he has often been considered his country’s greatest poet and the founder of modern Russian literature",

"Alexander Pushkin’s mother was the granddaughter of an Abyssinian prince, Hannibal, who had been a favorite of Peter I, and many of Pushkin’s forebears played important roles in Russian history. Pushkin began writing poetry as a student at the Lyceum at Tsarskoe Selo, a school for aristocratic youth.",
"Alexander Pushkin’s mother was the granddaughter of an Abyssinian prince, Hannibal, who had been a favorite of Peter I, and many of Pushkin’s forebears played important roles in Russian history. Pushkin began writing poetry as a student at the Louvre at Paris, a school for aristocratic youth.",

"Florida has a large retirement community, which tends to be more price-sensitive and focused on finding affordable homes."
]

correct = ['Alexander Sergeevich Pushkin <s>visited thailand in 2020<s>',
           'Aleksandr Sergeyevich Pushkin,  Russian poet, novelist, dramatist, and short-story writer; he has often been considered his country’s greatest poet and the founder <s>of modern french literature<s>',
           'Boris Galitsky is <s>ceo of microsoft<s>', 'Alexander Pushkin was <s>born in japan<s>',
           'Aleksandr Sergeyevich Pushkin born May 26  1799, Moscow, Russia and <s>died january 29 1837<s>, St. Petersburg',
           'Aleksandr Sergeyevich Pushkin,  Russian poet, novelist, dramatist, and short-story writer; he has often been considered his country’s greatest poet and the founder of modern Russian literature',
           'Alexander Pushkin’s mother was the granddaughter of an Abyssinian prince, Hannibal, who had been a favorite of Peter I, and many of Pushkin’s forebears played important roles in Russian history. Pushkin began writing poetry as a student at the Lyceum at Tsarskoe Selo, a school for aristocratic youth.',
           'Alexander Pushkin’s mother was the granddaughter of an Abyssinian prince, Hannibal, who had been a favorite of Peter I, and many of Pushkin’s forebears played important roles in Russian history. Pushkin began writing poetry as a <s>student at the louvre at paris, a school for aristocratic youth<s>.',
           'Florida has a large retirement community, which tends to be more price-sensitive and focused on finding affordable homes.']


results = []
count = 0
for sent in sentences:
    hetml, result = fact_checker.fact_check_sentence(sent, "")
    results.append(result)
    assert(result == correct[count])
    count+=1

print(results)



sentences1 = [ 'The deepest cave in the world is the "Veryovkina Cave" located in Abkhazia, Georgia, with a depth of 2,212 meters (7,257 feet). The expeditions to explore the cave have been led by the Ukrainian Speleological Association, with diver Gennadiy Samokhin leading the dives to reach the cave\'s lower depths',
    "Contextual raises $20m to bring retrieval augmented generation to the enterprise (4 minute read)",
    "Ex-Meta Researchers Have Raised $40 Million From Lux Capital For An AI Biotech Startup (6 minute read)",
              "Healthcare discourse analysis. ",
              "Corporate discourse analysis. ",
              "Discourse analysis can be used to analyze social justice issues, including race, gender, sexuality. ",
              "discourse analysis is a versatile method that can be applied to a wide range of social phenomena. ",
              "Failure by regulatory authorities to adequately supervise and enforce regulations can contribute to a bank's failure. ",
              "Fraud and corruption within a bank can lead to its failure. "
]

correct1 = ['Alexander Sergeevich Pushkin <s>visited thailand in 2020<s>',
           'Aleksandr Sergeyevich Pushkin,  Russian poet, novelist, dramatist, and short-story writer; he has often been considered his country’s greatest poet and the <s>founder of modern french literature<s>',
           'Boris Galitsky is <s>ceo of microsoft<s>', 'Alexander Pushkin was <s>born in japan<s>',
           'Aleksandr Sergeyevich Pushkin born May 26  1799, Moscow, Russia and <s>died january 29 1837<s>, St. Petersburg',
           'Aleksandr Sergeyevich Pushkin,  Russian poet, novelist, dramatist, and short-story writer; he has often been considered his country’s greatest poet and the founder of modern Russian literature',
           'Alexander Pushkin’s mother was the granddaughter of an Abyssinian prince, Hannibal, who had been a favorite of Peter I, and many of Pushkin’s forebears played important roles in Russian history. Pushkin began writing poetry as a student at the Lyceum at Tsarskoe Selo, a school for aristocratic youth.',
           'Alexander Pushkin’s mother was the granddaughter of an Abyssinian prince, Hannibal, who had been a favorite of Peter I, and many of Pushkin’s forebears played important roles in Russian history. Pushkin began writing poetry as a <s>student at the louvre at paris, a school for aristocratic youth<s>.',
           'Florida has a large retirement community, which tends to be more price-sensitive and focused on finding affordable homes.',
           'Boris Galitsky contributed semiconductor technologies to Silicon Valley startups as well as companies like eBay and Oracle']


results1 = ['The deepest cave in the world is the "Veryovkina Cave" located in Abkhazia, Georgia, with a depth of 2,212 meters (7,257 feet). <s>the expeditions to explore the cave<s> have been led by the <s>ukrainian speleological association<s>, with <s>diver gennadiy samokhin<s> leading the <s>dives<s> to reach the cave\'s lower depths',
           'Contextual raises $20m to bring retrieval augmented generation to the enterprise (<s>4 minute read<s>)',
           'Ex-Meta Researchers Have Raised $40 Million From Lux Capital For An AI Biotech Startup (<s>6 minute read<s>)',
           'Healthcare discourse analysis. ',
           '<s>corporate discourse analysis<s>. ',
           'Discourse analysis can be used to analyze <s>social justice issues, including race, gender, sexuality<s>. ',
           'discourse analysis is a versatile method that can be applied to a <s>wide range of social phenomena<s>. ',
           "<s>failure by regulatory authorities<s> to adequately supervise and enforce regulations can contribute to a bank's failure. ",
           '<s>fraud and corruption within a bank<s> can lead to its failure. ',
           'Boris Galitsky contributed semiconductor technologies to Silicon Valley startups as well as companies like eBay and Oracle']


count = 0
for sent in sentences1:
    html, result = fact_checker.fact_check_sentence(sent, "")
    results.append(result)
    if not result == correct[count]:
        print(result)
    #assert(result == correct[count])
    count+=1

