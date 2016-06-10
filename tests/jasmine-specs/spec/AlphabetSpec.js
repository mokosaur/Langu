describe("Letters wheel", function() {
    var wheel;

    beforeEach(function() {
        wheel = new LettersWheel([['a', 'a'], ['be', 'b'], ['ce', 'c'], ['de', 'd'], ['e', 'e']]);
    });

    it("should have proper length", function() {
        expect(wheel.getLength()).toEqual(5);
    });

    it("should be iterable", function() {
        expect(wheel.iterator.hasNext()).toEqual(true);
        expect(wheel.iterator.getNext()[1]).toMatch(/[abcde]/);
        expect(wheel.getLength()).toEqual(5);
    });

    it("should show letter names", function() {
        expect(wheel.getLetterName(1)).toEqual('be');
    });

    it("should show letters", function() {
        expect(wheel.getLetter(1)).toEqual('b');
    });

    it("should give current letter", function() {
        wheel.chooseNextAnswer();
        expect(wheel.getCurrentLetter()).toMatch(/[abcde]/);
        expect(['a', 'be', 'ce', 'de', 'e']).toContain(wheel.getCurrentLetterName());
    });

    it("should shuffle properly", function() {
        var array = [1, 2, 3, 4, 5];
        shuffle(array);
        expect(array.length).toEqual(5);

        array = [];
        shuffle(array);
        expect(array).toEqual([]);

        array = ['a', 'l', 'a', 'm', 'a', 'k', 'o', 't', 'a'];
        shuffle(array);
        expect(array).toContain('l');
        expect(array).not.toContain('b');
    });
});

describe("Letters pool", function() {
    var pool;
    var letter;

    beforeEach(function() {
        pool = new LettersPool();
    });

    it("should allow to add letters", function() {
        pool.newLetter("test", "Red", 2);
        expect(pool.active.length).toEqual(1);
    });
    
    it("moves letters to passive state when removed", function() {
        letter = pool.newLetter("test", "Red", 2);
        pool.removeLetter(letter);
        expect(pool.active.length).toEqual(0);
        expect(pool.passive.length).toEqual(1);
    });

    it("should reuse used letters", function() {
        redLetter = pool.newLetter("test", "Red", 2);
        blueLetter = pool.newLetter("test", "Blue", 2);
        greenLetter = pool.newLetter("test", "Green", 2);
        pool.removeLetter(blueLetter);
        pinkLetter = pool.newLetter("test", "Pink", 2);
        expect(pool.active.length).toEqual(3);
        expect(pool.passive.length).toEqual(0);
    });

    it("constructs new letters properly", function() {
        letter = pool.newLetter("test", "Red", 2);
        expect(letter.text).toEqual("test");
        expect(letter.color).toEqual("Red");
        expect(letter.radius).toEqual(2);
    });

    it("reconstructs new letters properly", function() {
        letter = pool.newLetter("yo", "Blue", 5);
        pool.removeLetter(letter);
        letter = pool.newLetter("test", "Red", 2);
        expect(letter.text).toEqual("test");
        expect(letter.color).toEqual("Red");
        expect(letter.radius).toEqual(2);
    });
});