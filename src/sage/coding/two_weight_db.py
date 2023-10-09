# sage.doctest: optional - sage.modules sage.rings.finite_rings
r"""
Database of two-weight codes

This module stores a database of two-weight codes.

{DB_INDEX}

REFERENCE:

- [BS2003]_

- [ChenDB]_

- [Koh2007]_

- [Di2000]_

TESTS:

Check the data's consistency::

    sage: from sage.coding.two_weight_db import data
    sage: for code in data:
    ....:     M = code['M']
    ....:     assert code['n'] == M.ncols()
    ....:     assert code['k'] == M.nrows()
    ....:     w1,w2 = [w for w,f in enumerate(LinearCode(M).weight_distribution()) if w and f]
    ....:     assert (code['w1'], code['w2']) == (w1, w2)

"""
from sage.rings.finite_rings.finite_field_constructor import FiniteField as GF
from sage.matrix.constructor import Matrix

# The following is a list of two-weight codes stored as dictionaries. Each entry
# sets the base field, the matrix and the source: other parameters are computed
# automatically


data = [
    {
        'n' : 68,
        'k' : 8,
        'w1': 32,
        'w2': 40,
        'K' : GF(2),
        'M' : ("10000000100111100110000001101000100111000011100101011010111111010110",
               "01000000010011110011000000110100010011100001110010101101011111101011",
               "00100000001001111101100000011010001001110000111001010110101111110101",
               "00010000100011011100110001100101100011111011111001100001101000101100",
               "00001000110110001100011001011010011110111110011001111010001011000000",
               "00000100111100100000001101000101101000011100101001110111111010110110",
               "00000010011110010000000110100010111100001110010100101011111101011011",
               "00000001001111001100000011010001011110000111001010010101111110101101"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 140,
        'k' : 6,
        'w1': 90,
        'w2': 99,
        'K' : GF(3),
        'M' : ("10111011111111101110101110111100111011111011101111101001001111011011011111100100111101000111101111101100011011001111101110111110101111111001",
               "01220121111211011101011101112101220022120121011222010110011010120110112112001101021010101111012211011000020110012221212101011101211122020011",
               "22102021112110111120211021122012100012202220112110101200110101202102122120011110020201211110021210110000101200121222122010211022211210110101",
               "11010221121101111102210221220221000111011101121102012101101012012022222000211200202012211100111201200001122001211011120102110212212102121001",
               "20201121211111111012202022201210001220122121211010121011010020110121220201212002010222011001111012100011010212110021202021102112221012110011",
               "02022222111111110112020112011200022102212222110102210110100101102211201211220020002120110011110221100110002121100222120211021112010112220101"),
        'source': "Found by Axel Kohnert [Koh2007]_ and shared by Alfred Wassermann.",
    },
    {
        'n' : 98,
        'k' : 6,
        'w1': 63,
        'w2': 72,
        'K' : GF(3),
        'M' : ("10000021022112121121110122000110112002010011100120022110120200120111220220122120012012100201110210",
               "01000020121020200200211101202121120002211002210100021021202220112122012212101102010210010221221201",
               "00100021001211011111111202120022221002201111021101021212210122101020121111002000210000101222202000",
               "00010022122200222202201212211112001102200112202202121201211212010210202001222120000002110021000110",
               "00001021201002010011020210221221012112200012020011201200111021021102212120211102012002011201210221",
               "00000120112212122122202110022202210010200022002120112200101002202221111102110100210212001022201202"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 84,
        'k' : 6,
        'w1': 54,
        'w2': 63,
        'K' : GF(3),
        'M' : ("100000210221121211211212100002020022102220010202100220112211111022012202220001210020",
               "010000201210202002002200010022222022012112111222010212120102222221210102112001001022",
               "001000210012110111111202101021212221000101021021021211021221000111100202101200010122",
               "000100221222002222022202010121111210202200012001222011212000211200122202100120211002",
               "000010212010020100110002001011101112122110211102212121200111102212021122100010201120",
               "000001201122121221222212000110100102011101201012001102201222221110211011100001200102"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 56,
        'k' : 6,
        'w1': 36,
        'w2': 45,
        'K' : GF(3),
        'M' : ("10000021022112022210202200202122221120200112100200111102",
               "01000020121020221101202120220001110202220110010222122212",
               "00100021001211211020022112222122002210122100101222020020",
               "00010022122200010012221111121001121211212002110020010101",
               "00001021201002220211121011010222000111021002011201112112",
               "00000120112212111201011001002111121101002212001022222010"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 65,
        'k' : 4,
        'w1': 50,
        'w2': 55,
        'K' : GF(5),
        'M' : ("10004323434444234221223441130101034431234004441141003110400203240",
               "01003023101220331314013121123212111200011403221341101031340421204",
               "00104120244011212302124203142422240001230144213220111213034240310",
               "00012321211123213343321143204040211243210011144140014401003023101"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 52,
        'k' : 4,
        'w1': 40,
        'w2': 45,
        'K' : GF(5),
        'M' : ("1000432343444423422122344123113041011022221414310431",
               "0100302310122033131401312133032331123141114414001300",
               "0010412024401121230212420301411224123332332300210011",
               "0001232121112321334332114324420140440343341412401244"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 39,
        'k' : 4,
        'w1': 30,
        'w2': 35,
        'K' : GF(5),
        'M' : ("111111111111111111111111111111000000000",
               "111111222222333333444444000000111111000",
               "223300133440112240112240133440123400110",
               "402340414201142301132013234230044330401"),
        'source': "From Bouyukliev and Simonis ([BS2003]_, Theorem 4.1)",
    },
    {
        'n' : 55,
        'k' : 5,
        'w1': 36,
        'w2': 45,
        'K' : GF(3),
        'M' : ("1000010122200120121002211022111101011212112022022020002",
               "0100011101120102100102202121022211112000020211221222002",
               "0010021021222220122011212220021121100021220002100102201",
               "0001012221012012100200102211110211121211201002202000222",
               "0000101222101201210020110221111020112121120120220200022"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 126,
        'k' : 6,
        'w1': 81,
        'w2': 90,
        'K' : GF(3),
        'M' : ("100000210221121211211101220021210000100011020200201101121021122102020111100122122221120200110001010222000021110110011211110210",
               "010000201210202002002111012020001001110012222220221211200120201212222102210100001110202220121001110211200120221121012001221201",
               "001000210012110111111112021220210102211012212122200222212000112220212011021102122002210122122101120210120100102212112112202000",
               "000100221222002222022012122120201012021112211112111120010221100121011012202201001121211212002211120210012201120021222121000110",
               "000010212010020100110202102200200102002122111011112210121010202111121212020010222000111021000222122210001011222102100121210221",
               "000001201122121221222021100221200012000220101001022022100122112010102222002122111121101002200020221110000122202000221222201202"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 154,
        'k' : 6,
        'w1': 99,
        'w2': 108,
        'K' : GF(3),
        'M' : ("10000021022112121121110122002121000010001102020020110112102112202221021020201" +
               "20202212102220222022222110122210022201211222111110211101121002011102101111002",
               "01000020121020200200211101202000100111001222222022121120012020122110122122221" +
               "02222102012112111221111021101101021121002001022221202211100102212212010222102",
               "00100021001211011111111202122021010221101221212220022221200011221102002202120" +
               "20121121000101000111020212200020121210011112210001001022001012222020000100212",
               "00010022122200222202201212212020101202111221111211112001022110001001221210110" +
               "12211020202200222000021101010212001022212020002112011200021100210001100121020",
               "00001021201002010011020210220020010200212211101111221012101020222021111111212" +
               "11120012122110211222201220220201222200102101111020112221020112012102211120101",
               "00000120112212122122202110022120001200022010100102202210012211211120100101022" +
               "01011212011101110111112202111200111021221112222211222020120010222012022220012"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 198,
        'k' : 10,
        'w1': 96,
        'w2': 112,
        'K' : GF(2),
        'M' : ("1000000000111111101010000100011001111101101010010010011110001101111001101100111000111101010101110011" +
               "11110010100111101001001100111101011110111100101101110100111100011111011011100111110010100110110000",
               "0100000000010110011100100010101010101111011010001001010110011010101011011101000110000001101101010110" +
               "10110111110101000000011011001100010111110001001011011100111100100000110001011001110110011101011000",
               "0010000000011100111110111011000011010100100011110000001100011011101111001010001100110110000001111000" +
               "11000000101011010111110101000111110010011011101110000010110100000011100010011111100100111101010010",
               "0001000000001111100010000000100101010001110111100010010010010111000100101100010001001110111101110100" +
               "10010101101100110011010011101100110100100011011101100000110011110011111000000010110101011111101111",
               "0000100000110010010000010110000111010011010101000010110100101010011011000011001100001110011011110001" +
               "11101000010000111101101100111100001011010010111011100101101001111000100011000010110111111111011100",
               "0000010000110100111001111011010000101110001011100010010010010111100101011001011011100110101110100001" +
               "01101010110010100011000101111100100001110111001001001001001100001101110110000110101010011010101101",
               "0000001000011011110010110100010010001100000011001000011101000110001101001000110110010101011011001111" +
               "01111111010011111010100110011001110001001000001110000110111011010000011101001110111001011011001011",
               "0000000100111001101011110010111100100001010100100110001100100110010101111001100101101001000101011000" +
               "10001001111101011101001001010111010011011101010011010000101010011001010110011110010000011011111001",
               "0000000010101011010101010101011100111101111110100011011001001010111101100111010110100101100110101100" +
               "00000001100011110110010101100001000000010100001101111011111000110001100101101010000001110101011100",
               "0000000001101100111101011000010000000011010100000110101010011010100111100001000011010011011101110111" +
               "01110111011110101100100100110110011100001001000001010011010010010111110011101011101001101101011010"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 219,
        'k' : 9,
        'w1': 96,
        'w2': 112,
        'K' : GF(2),
        'M' : ("10100011001110100010100010010000100100001011110010001010011000000001101011110011001001000010011110111011111" +
               "0001001010110110110111001100111100011011101000000110101110001010100011110011111111110111010100101011000101111111",
               "01100010110101110100001000010110001010010010011000111101111001011101000011101011100111111110001100000111010" +
               "1101001000110001111011001100101011110101011110010001101011110000100000101101100010110100001111001100110011001111",
               "00010010001001011011001110011101111110000000101110101000110110011001110101011011101011011011000010010011111" +
               "1110110100111111000000110011101101000000001010000000011000111111100101100001110011110001110011110110100111100001",
               "00001000100010101110101110011100010101110011010110000001111111100111010000101110001010100100000001011010111" +
               "1001001000000011000011001100100100111010000000001010111001001100100101011110001100110001000000111001100100100111",
               "00000101010100010101101110011101001000101110000000000111101100011000000001110100000001011010101001111110110" +
               "0010110111100111000000110011110110101101110000001111100001010001100101100001110011110001101101000000000000100001",
               "00000000000000000000010000011101011100100010000110110100101011001011001100000001011000101010100111000111101" +
               "0011100011011011011111100010011100010111101001011001001101100010011010001011010110001110100001001111110010100100",
               "00000000000000000000000001011010110110101111010110101001001001000101010000000000001011000011000010100100110" +
               "0000110000111101100010000111111111101101001010110000111111101110101011010010010001011101110011111001100100101110",
               "00000000000000000000000000110111101011110010101110000110010010100010001010000000010100011000101000010011000" +
               "0110000111100110100001001011111111111010110000001010111111110011110110001100100010101011101101110110011000110110",
               "00000000000000000000000000000000000000000000000001111111111111111111111110000001111111111111111111111111111" +
               "1111111100000000000011111111111111000000111111111111111111000000000000111111111111000000000000000000111111000110"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 73,
        'k' : 9,
        'w1': 32,
        'w2': 40,
        'K' : GF(2),
        'M' : ("1010010100000010100000101010001100110101101101000010110010100100111011101",
               "0110000110000101101111001101000100111111101011011101110010110001100111100",
               "0001010000000001111111011010100101001111011010101100001010000001110100001",
               "0000100100000001111111100111000011110011110101000001010110000001011010001",
               "0000001010000001111110111100011000111100101110010010101100000001101001001",
               "0000000001000111001010110010011001101001011010110110011001010111100010010",
               "0000000000100100011000100100111100001100101111010001011011111000110011110",
               "0000000000010111001100101011111110101010000000000100111110000001111111100",
               "0000000000001011100001000011011010110001110101101100001100101110101110110"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 70,
        'k' : 9,
        'w1': 32,
        'w2': 40,
        'K' : GF(2),
        'M' : ("0100011110111000001011010110110111100010001000001000001001010110101101",
               "1000111101110000000110101111101111000100010000010000000010101111001011",
               "0001111011100000011101011101011110011000100000100000000101011100010111",
               "0011110101000000111010111010111100110001000011000000001010111000101101",
               "0111101000000001110101110111111001100010000100000000010101110011001011",
               "1111010000000011101011101101110011010100001000000000101011100100010111",
               "1110100010000111000111011011100110111000010000000001000111001010101101",
               "1101000110001110001110110101001101110000100010000010001110010101001011",
               "1010001110011100001101101010011011110001000100000100001100101010010111"),
        'source': "Found by Axel Kohnert [Koh2007]_ and shared by Alfred Wassermann.",
    },
    {
        'n' : 85,
        'k' : 8,
        'w1': 40,
        'w2': 48,
        'K' : GF(2),
        'M' : ("1000000010011101010001000011100111000111111010110001101101000110010011001101011100001",
               "0100000011010011111001100010010100100100000111101001011011100101011010101011110010001",
               "0010000011110100101101110010101101010101111001000101000000110100111110011000100101001",
               "0001000011100111000111111010110001101101000110010011001101011100001100000001001110101",
               "0000100011101110110010111110111111110001011001111000001011101000010101001101111011011",
               "0000010011101010001000011100111000111111010110001101101000110010011001101011100001100",
               "0000001001110101000100001110011100011111101011000110110100011001001100110101110000110",
               "0000000100111010100010000111001110001111110101100011011010001100100110011010111000011"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 15,
        'k' : 4,
        'w1': 9,
        'w2': 12,
        'K' : GF(3),
        'M' : ("100022021001111",
               "010011211122000",
               "001021112100011",
               "000110120222220"),
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 34,
        'k' : 4,
        'w1': 24,
        'w2': 28,
        'K' : GF(4,name='x'),
        'M' : [[1,0,0,0,  1,'x', 'x','x^2',  1,  0,  'x','x',  0,    1,'x^2','x','x','x^2','x^2','x^2','x',  'x','x^2','x^2','x^2',    1,'x^2','x',1,0,  1,  'x','x^2',    1],
               [0,1,0,0,'x','x',   1,'x^2',  1,  1,'x^2',  1,'x',  'x',    0,  0,  1,    0,  'x',  'x',  0,    1,'x^2',  'x',  'x',    1,    0,  0,0,1,'x',  'x','x^2',    1],
               [0,0,1,0,  1,  0,   0,  'x','x',  1,'x^2',  1,  1,'x^2',    1,'x','x',  'x','x^2',    1,  0,  'x',  'x',    0,    1,'x^2',  'x','x',1,0,  0,    0,    1,  'x'],
               [0,0,0,1,'x','x','x^2',   1,  0,'x',  'x',  0,  1,'x^2',  'x','x',  1,'x^2','x^2',  'x','x','x^2','x^2','x^2',    1,'x^2',  'x',  1,0,1,'x','x^2',    1,'x^2']],
        'source': "Shared by Eric Chen [ChenDB]_.",
    },
    {
        'n' : 121,
        'k' : 5,
        'w1': 88,
        'w2': 96,
        'K' : GF(4,name='x'),
        'M' : [map({'0':0,'1':1,'a':'x','b':'x**2'}.get,x) for x in
               ["11b1aab0a0101010b1b0a0bab0a0a0b011a0a1b1aab0b1a0b1bab0b0a0b1b011a011a011a011b0b1b0b0b0b0aab1a1b0aab0b010aab1a010b0a1a1aab",
                "01100110011aa0011aabb0011bb11aabb00bb00aabb11bb11aa0011aabb00aabb00aabb0011bb0011aa00aabb0011aa11aabb00aabb0011aabb00aabb",
                "000111100000011111111aaaaaabbbbbb0000111111aaaabbbb00000000111111aaaaaabbbbbb000000111111aaaaaa000000111111aaaaaaaabbbbbb",
                "00000001111111111111111111111111100000000000000000011111111111111111111111111aaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbb",
                "0000000000000000000000000000000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
               ]],
        'source' : "From [Di2000]_",
    },
    {
        'n' : 132,
        'k' : 5,
        'w1': 96,
        'w2': 104,
        'K' : GF(4,name='x'),
        'M' : [map({'0':0,'1':1,'a':'x','b':'x**2'}.get,x) for x in
               ["aab1a1ab0b11b1a10b0b101ab00ab1b01ab01abbabab10a1b0a0101a1a1a01ab1b0101ab01ba00bb1bb111b11b1011b1ab0abb1b01abab00abab0aab01001ab0a11b",
                "10011b0011abb001aaaab00001ab011aaaabbbb1aabb011aabb001aabb01a00abb001111bbb01aab001ab001bb011aa011aaab001111aab00abb0011aab000011abb",
                "011111000000011111aaabbbbbbb0000000000011111aaaaaaabbbbbbb00011111aaaaaaaaabbbbb0000011111aaaaabbbbbbb00000000011111aaaaaaabbbbbbbbb",
                "00000011111111111111111111110000000000000000000000000000001111111111111111111111aaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
               ]],
        'source' : "From [Di2000]_",
    },
    {
        'n' : 143,
        'k' : 5,
        'w1': 104,
        'w2': 112,
        'K' : GF(4,name='x'),
        'M' : [map({'0':0,'1':1,'a':'x','b':'x**2'}.get,x) for x in
               ["1a01a01ab0aaab0bab0a1ab0bab0ab0a01a0a011aab00a01a1a011b00101b1a1bb0a0abab00a1a01a1b11a010b01ab1ab0a011a01ab00a10b0a01babab1a1ba011ab0a1ab0a0b01",
                "0011abbbb001aabb00aabbb0011aaabb00011bb0011abb000aabb001aa00b11aab00111aa0110011abb0aabb001111aaabb0011aaaab001bb00111aa0011aab11aaabb00011aabb",
                "11111111100000001111111aaaaaaaaabbbbbbb00000001111111aaaaabbb000001111111aaabbbbbbb0000011111111111aaaaaaaaabbbbb00000001111111aaaaaaabbbbbbbbb",
                "00000000011111111111111111111111111111100000000000000000000001111111111111111111111aaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "00000000000000000000000000000000000000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
               ]],
        'source' : "From [Di2000]_",
    },
    {
        'n' : 168,
        'k' : 6,
        'w1': 108,
        'w2': 117,
        'K' : GF(3),
        'M' : ["101212212122202012010102120101112012121001201012120220122112001121201201201201010020012201001201201201202120121122012021201221021110200212121011211002012220000122201201",
               "011100122001200111220011220020011222001200022000220012220122011220011101122012012001222010122200012011120112220112000120120012002012201122001220012122000201212001211211",
               "000011111000011111112000001112000000111122222000001111112222000001111122222000111222222001111122222000001111112222000001112222000111122222000001111222000011122000011122",
               "000000000111111111111000000000111111111111111222222222222222000000000000000111111111111222222222222000000000000000111111111111222222222222000000000000111111111222222222",
               "000000000000000000000111111111111111111111111111111111111111000000000000000000000000000000000000000111111111111111111111111111111111111111222222222222222222222222222222",
               "000000000000000000000000000000000000000000000000000000000000111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"],
        'source' : "From [Di2000]_",
    },
]

# Build actual matrices.
for code in data:
    code['M'] = Matrix(code['K'],[list(R) for R in code['M']])

DB_INDEX = (".. csv-table::\n"
            "   :class: contentstable\n"
            "   :widths: 7,7,7,7,7,50\n"
            "   :delim: @\n\n")

data.sort(key=lambda x:(x['K'].cardinality(),x['k'],x['n']))
for x in data:
    s = "    `q={}` @ `n={}` @ `k={}` @ `w_1={}` @ `w_2={}` @ {}\n".format(x['K'].cardinality(),x['n'],x['k'],x['w1'],x['w2'],x.get('source',''))
    DB_INDEX += s

__doc__ = __doc__.format(DB_INDEX=DB_INDEX)
