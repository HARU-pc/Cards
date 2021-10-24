from setuptools import setup

setup(
    name="Playing_cards",
    version="1.0.0",
    description="You can enjoy playing some playing cards games.",
    long_description="You can enjoy playing blacjack on cli.\nI'll give you more games.\n",
    url='https://twitter.com/HARU_4538',
    author='ホッカｲﾓ',
    author_email='4538haru@gmail.com',
    classifiers=[
        # パッケージのカテゴリー
        # https://pypi.python.org/pypi?:action=list_classifiers
        # から該当しそなもを選んでおけばよい。
        "Topic :: Games/Entertainment"
    ],
    keywords='playingcard',
    install_requires=["numpy","dll","pycryptodome"],
)