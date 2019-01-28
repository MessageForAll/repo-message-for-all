import codecs


s = '1f602'
with codecs.open('test.out', 'w', 'utf-8') as outfile:
    outfile.write('{}\n'.format(eval('u"{}{}"'.format(r'\U000', text))))
