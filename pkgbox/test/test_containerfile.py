from pkgbox import containerfile


def test_load(fixdir):
    expected = containerfile.Containerfile('FROM registry.fedoraproject.org/fedora:40')
    with open(f'{fixdir}/Containerfile', 'r') as f:
        actual = containerfile.load(f) 
    
    assert expected == actual


def test_loads(fixdir):
    expected = containerfile.Containerfile('FROM registry.fedoraproject.org/fedora:40')
    with open(f'{fixdir}/Containerfile', 'r') as f:
        data = f.read()

    assert expected == containerfile.loads(data)


def test_instruction_from()
