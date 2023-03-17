from .amr_processor import AmrProcessor

if __name__ == '__main__':
    text = [
        "To assist Jeff Henry at Chime in partnering with various community organizations. This is to enter into collaborative programmatic efforts related to financial literacy, scholarships, and microgrants. "]
    instance = AmrProcessor()
    graphs = instance.amr_parse(text)
    names = instance.extract_names(graphs)
    print(names)
    assert (len(names) > 2)

    # todo 'Ownership of KMS Property: Kim Malone Scott ("KMS") has developed, among other things, a unique management philosophy and certain related management and training approaches
